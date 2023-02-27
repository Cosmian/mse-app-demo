"""app module."""

import base64
import io
import logging
import multiprocessing
import os
import threading
from http import HTTPStatus, client
from typing import Any, Optional

import numpy as np
from flask import Flask, Response, jsonify, request
from flask_cors import CORS
from keras.models import load_model
from PIL import Image

app = Flask(__name__)
cors = CORS(app)

logging.basicConfig(
    format="[%(levelname)s] %(message)s",
    level=logging.DEBUG
)

CWD_PATH = os.getenv("MODULE_PATH")
if (CWD_PATH == None):
    model = load_model(f"./mnist.h5")
else:
    model = load_model(f"{CWD_PATH}/mnist.h5")

@app.post("/")
def push():
    data: Optional[Any] = request.get_json(silent=True)
    if (not data or not data['data']):
        app.logger.error("No data part")
        return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)
    if (len(data['data'].split("data:image/png;base64,")) < 2):
        app.logger.error("Wrong data format")
        return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)
    imgString = data['data'].split("data:image/png;base64,")[1]
    imgData = base64.b64decode(imgString)
    img = Image.open(io.BytesIO(imgData))

    img = img.resize((28,28))
    img = img.convert('L')
    img = np.array(img)
    img = (img / 255)
    img = np.array([img])

    res = model.predict([img])
    res = np.argmax(res[0])

    response = jsonify({"number": str(res)})
    return response

@app.get("/health")
def health_check():
    """Health check of the application."""
    return Response(status=HTTPStatus.OK)
