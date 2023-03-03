"""`Digit recognition` example."""

import logging
import os
from http import HTTPStatus
from typing import Any, Optional

from flask import Flask, Response, jsonify, request
from flask.logging import create_logger
from flask_cors import CORS
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

app = Flask(__name__)
cors = CORS(app)
LOG = create_logger(app)

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.DEBUG)

CWD_PATH = os.getenv("MODULE_PATH")
model = AutoModelForSequenceClassification.from_pretrained(
    f"{CWD_PATH}/lvwerra/distilbert-imdb_local_model"
)
tokenizer = AutoTokenizer.from_pretrained(
    f"{CWD_PATH}/lvwerra/distilbert-imdb_local_tokenizer"
)


@app.post("/")
def predict_sentiment():
    """Predict sentiment"""
    data: Optional[Any] = request.get_json(silent=True)
    if not data or not data["data"]:
        LOG.error("No data part")
        return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)

    phrase = data["data"]
    classifier = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
    result = classifier(phrase)[0]

    response = jsonify({"sentiment": f"{result['label']}"})
    return response


@app.get("/health")
def health_check():
    """Health check of the application."""
    return Response(response="OK", status=HTTPStatus.OK)
