import os
from dotenv import load_dotenv
from flask import request, abort
from functools import wraps


def require_key(flask_route):
    """
    Checks that the request includes an API key in the auth headers
    @returns a decorated function on success, a 401 error if the header isn't present
    """

    @wraps(flask_route)
    def decorated(*args, **kwargs):
        secret_key = "Bearer " + os.environ.get("API_KEY")

        if request.headers.get("Authorization") == secret_key:
            return flask_route(*args, **kwargs)
        else:
            return abort(401)

    return decorated
