def repo_name(wid, cid):
    return "{}-{}".format(wid, cid)


def change_ref(sid, uid, change_id):
    return "{}/{}/{}".format(sid, uid, change_id)


def plan_ref(sid, uid, change_id):
    return "tf/plan/{}".format(change_ref(sid, uid, change_id))


def apply_ref(sid):
    return "tf/apply/{}".format(sid)
