"""app module."""

from http import HTTPStatus
import logging
from typing import Optional, Any

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
    """Add a number to the global mean."""
    data: Optional[Any] = request.get_json(silent=True)

    if data is None or not isinstance(data, dict):
        app.logger.error("TypeError with data: '%s'", data)
        return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)
    
    n: Optional[float] = data.get("n")

    if n is None or not isinstance(n, (float, int)):
        app.logger.error("TypeError with data content: '%s' (%s)", n, type(n))
        return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)

    globs.COUNT += 1
    globs.AVERAGE += n

    app.logger.info("Successfully added %s", n)
    return Response(status=HTTPStatus.OK)


@app.get("/")
def mean():
    """Get the current mean."""
    if globs.COUNT < 2:
        app.logger.error("need more than 2 values to compute the mean")
        return {"mean": None, "count": globs.COUNT}

    return {"mean": globs.AVERAGE / globs.COUNT, "count": globs.COUNT}


@app.delete("/")
def reset():
    """Reset the current mean."""
    globs.AVERAGE = 0.0
    globs.COUNT = 0

    app.logger.info("Reset successfully")

    return Response(status=HTTPStatus.OK)
