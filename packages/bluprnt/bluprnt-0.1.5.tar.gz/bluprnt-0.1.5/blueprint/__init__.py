import logging
import os
import json
from base64 import urlsafe_b64decode
import requests
from requests.exceptions import HTTPError
from flask import Request, jsonify, abort


MEDIATOR_URL = os.environ["MEDIATOR_URL"]


def _get_auth_token(audience):
    token_url = (
        "http://metadata.google.internal"
        "/computeMetadata/v1/instance/service-accounts/default/identity"
        f"?audience={audience}"
    )
    return requests.get(
        url=token_url, headers={"Metadata-Flavor": "Google"},
    ).content.decode()


def call(service_name, service_path=None, **kwargs):
    auth = {"Authorization": "Bearer " + _get_auth_token(MEDIATOR_URL)}
    r = requests.post(MEDIATOR_URL, headers=auth, json=kwargs)
    if r.status_code >= 500:
        r.raise_for_status()
    return r


def user_info(request: Request):
    encoded_user_info = request.headers.get("X-Endpoint-Api-Userinfo")
    if encoded_user_info:
        if not encoded_user_info.endswith("=="):
            encoded_user_info += "=="
        return json.loads(urlsafe_b64decode(encoded_user_info))
    return {}


def auth(permission):
    def wrap(func):
        def wrapped_func(request: Request):
            try:
                r = call(
                    "db",
                    "authorize",
                    asset=request.json["asset"],
                    uid=user_info(request)["user_id"],
                    permission=permission,
                )
                r.raise_for_status()
                if not r.json()["granted"]:
                    resp = jsonify(message="Access denied.")
                    resp.status_code = 403
                    abort(resp)
            except HTTPError as e:
                logging.exception(e)
                resp = jsonify(message="An unexpected error occurred in authorization.")
                resp.status_code = 500
                abort(resp)
            return func(request)

        return wrapped_func

    return wrap


def _trim_document_path(path):
    return "/".join(path.split("/")[5:])


def repo_name(wid, cid):
    return "{}-{}".format(wid, cid)


class Asset:
    def __init__(self, path):
        self.path = path
        path_parts = self.path.split("/")
        self.id = path_parts[-1]
        self.type = path_parts[-2]
        if len(path_parts) > 2:
            self.parent = Asset("/".join(path_parts[:-2]))
        else:
            self.parent = None


class ParsedRequest:
    def __init__(self, request: Request):
        data = request.json
        self.user_info = user_info(request)
        self.data = data
        self.repo = repo_name(data.get("wid"), data.get("cid"))
        self.change_ref = "{}/{}/{}".format(
            data.get("sid"), self.user_info.get("user_id"), data.get("change_id")
        )
        self.plan_ref = "tf/plan/{}".format(self.change_ref)
        self.apply_ref = "tf/apply/{}".format(data.get("sid"))
        self.source_apply_ref = "tf/apply/{}".format(data.get("source_sid"))


class DBEvent:
    def __init__(self, event):
        value = event["value"] or event["oldValue"]
        self.asset = Asset(_trim_document_path(value["name"]))
        self.data = self._raise_values(value["fields"])

    def _raise_value(self, value_obj):
        value_type = next(iter(value_obj))
        if value_type == "mapValue":
            value = self._raise_values(value_obj[value_type])
        elif value_type == "arrayValue":
            value = [self._raise_value(v) for v in value_obj[value_type]["values"]]
        elif value_type == "referenceValue":
            value = Asset(_trim_document_path(value_obj[value_type]))
        else:
            value = value_obj[value_type]
        return value

    def _raise_values(self, fields):
        values = {}
        for key in fields:
            value_type = next(iter(fields[key]))
            values[key] = self._raise_value(fields[value_type])
        return values

