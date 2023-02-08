"""app module."""

import logging
from http import HTTPStatus
from typing import Any, Optional

from flask import Flask, Response, request

import globs

app = Flask(__name__)

logging.basicConfig(
    format="[%(levelname)s] %(message)s",
    level=logging.DEBUG
)


@app.get("/health")
def health_check():
    """Health check of the application."""
    return Response(status=HTTPStatus.OK)


@app.post("/")
def push():
    """Add a number to the pool."""
    data: Optional[Any] = request.get_json(silent=True)

    if data is None or not isinstance(data, dict):
        app.logger.error("TypeError with data: '%s'", data)
        return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)

    n: Optional[float] = data.get("n")

    if n is None or not isinstance(n, (float, int)):
        app.logger.error("TypeError with data content: '%s' (%s)", n, type(n))
        return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)

    globs.POOL.append(n)

    app.logger.info("Successfully added %s", n)
    return Response(status=HTTPStatus.OK)


@app.get("/")
def maximum():
    """Get the current max in pool."""
    if len(globs.POOL) < 1:
        app.logger.error("need more than 1 value to compute the max")
        return {"max": None}

    max_value = max(globs.POOL)
    index = globs.POOL.index(max_value)

    return {"max": "User #{}".format(index + 1)}


@app.delete("/")
def reset():
    """Reset the current pool."""
    globs.POOL = []

    app.logger.info("Reset successfully")

    return Response(status=HTTPStatus.OK)
