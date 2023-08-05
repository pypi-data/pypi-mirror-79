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


class ParsedRequest:
    def __init__(self, request: Request):
        data = request.json
        self.user_info = user_info(request)
        self.data = data
        self.repo = "{}-{}".format(data.get("wid"), data.get("cid"))
        self.change_ref = "{}/{}/{}".format(
            data.get("sid"), self.user_info.get("user_id"), data.get("change_id")
        )
        self.plan_ref = "tf/plan/{}".format(self.change_ref)
        self.apply_ref = "tf/apply/{}".format(data.get("sid"))
        self.source_apply_ref = "tf/apply/{}".format(data.get("source_sid"))
