from flask import abort


def bad_request(msg):
    """Answer to wrong request."""
    abort(400, msg)
