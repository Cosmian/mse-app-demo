from flask import make_response, request
from functools import wraps

PREFIX = "Bearer "


# Authentication decorator
def check_token(valid_token):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "Authorization" in request.headers:
                bearer_token = request.headers["Authorization"]
                if not bearer_token.startswith(PREFIX):
                    return make_response("Bearer not found!", 401)
                token = bearer_token[len(PREFIX) :]
                if token == valid_token:
                    return f(*args, **kwargs)
            return make_response("Invalid token!", 401)

        return wrapper

    return decorator
