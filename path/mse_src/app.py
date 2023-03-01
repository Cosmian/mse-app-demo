"""`Path` example."""

import json
import os
from datetime import datetime
from http import HTTPStatus
from pathlib import Path

from auth import check_token
from flask import Flask, Response

app = Flask(__name__)

WORKFILE: Path = Path(os.getenv("HOME")) / "date.txt"
SECRETS = json.loads(Path(os.getenv("SECRETS_PATH")).read_text(encoding="utf-8"))


@app.get("/health")
def health_check():
    """Health check of the application."""
    return Response(response="OK", status=HTTPStatus.OK)


@app.post("/")
@check_token(SECRETS["write_token"])
def write_date():
    """Write a simple file."""
    WORKFILE.write_text(str(datetime.now()))
    return Response(response="Date file written successfully", status=HTTPStatus.OK)


@app.route("/")
@check_token(SECRETS["read_token"])
def read_date():
    """Read a simple file."""
    if not WORKFILE.exists():
        return Response(
            response="You should write before read", status=HTTPStatus.NOT_FOUND
        )

    txt = WORKFILE.read_text()
    WORKFILE.unlink()

    return txt
