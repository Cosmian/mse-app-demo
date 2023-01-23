import os
import json

from http import HTTPStatus
from pathlib import Path
from datetime import datetime
from flask import Flask, Response

app = Flask(__name__)

WORKFILE: Path = Path(os.getenv("HOME")) / "date.txt"


@app.get("/health")
def health_check():
    """Health check of the application."""
    return Response(status=HTTPStatus.OK)


@app.route('/whoami')
def whoami():
    """A simple example manipulating secrets."""
    secrets = json.loads(Path(os.getenv("SECRETS_PATH")).read_text())
    return secrets["login"]


@app.post('/')
def write_date():
    """A simple example of file writing."""
    WORKFILE.write_text(str(datetime.now()))
    return Response(status=HTTPStatus.OK)


@app.route('/')
def read_date():
    """A simple example of file reading."""
    if not WORKFILE.exists():
        return Response(response="You should write before read",
                        status=HTTPStatus.NOT_FOUND)

    txt = WORKFILE.read_text()
    WORKFILE.unlink()

    return txt
