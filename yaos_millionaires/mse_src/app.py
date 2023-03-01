"""app module."""

import logging
from http import HTTPStatus
from typing import Any, Optional

import globs
from flask import Flask, Response, request
from flask.logging import create_logger

app = Flask(__name__)
LOG = create_logger(app)

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.DEBUG)


@app.get("/health")
def health_check():
    """Health check of the application."""
    return Response(response="OK", status=HTTPStatus.OK)


@app.post("/")
def push():
    """Add a number to the pool."""
    data: Optional[Any] = request.get_json(silent=True)

    if data is None or not isinstance(data, dict):
        LOG.error("TypeError with data: '%s'", data)
        return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)

    n: Optional[float] = data.get("n")

    if n is None or not isinstance(n, (float, int)):
        LOG.error("TypeError with data content: '%s' (%s)", n, type(n))
        return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)

    globs.POOL.append(n)

    LOG.info("Successfully added %s", n)
    return Response(status=HTTPStatus.OK)


@app.get("/")
def maximum():
    """Get the current max in pool."""
    if len(globs.POOL) < 1:
        LOG.error("need more than 1 value to compute the max")
        return {"max": None}

    max_value = max(globs.POOL)
    index = globs.POOL.index(max_value)

    return {"max": f"User #{index + 1}"}


@app.delete("/")
def reset():
    """Reset the current pool."""
    globs.POOL = []

    LOG.info("Reset successfully")

    return Response(status=HTTPStatus.OK)
