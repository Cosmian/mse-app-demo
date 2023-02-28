"""Authentication module."""

from functools import wraps

from flask import make_response, request

PREFIX = "Bearer "


def check_token(valid_token):
    """Verify the token from the HTTP header against a valid reference."""

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if "Authorization" in request.headers:
                bearer_token = request.headers["Authorization"]
                if not bearer_token.startswith(PREFIX):
                    return make_response("Bearer not found!", 401)
                prefix_length = len(PREFIX)
                token = bearer_token[prefix_length:]
                if token == valid_token:
                    return f(*args, **kwargs)
            return make_response("Invalid token!", 401)

        return wrapper

    return decorator
