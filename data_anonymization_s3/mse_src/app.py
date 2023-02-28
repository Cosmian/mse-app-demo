"""`Data anonymization using S3` example."""

import json
import os
from http import HTTPStatus
from io import BytesIO
from pathlib import Path
from typing import List, Optional

import boto3
import pandas as pd
from auth import check_token
from cosmian_lib_anonymization import anonymize_dataset
from flask import Flask, Response, make_response, request, send_file
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

app = Flask(__name__)
# set custom path for MSE
app.config["UPLOAD_FOLDER"] = os.getenv("TMP_PATH", "/tmp")
CONFIG_FILE = Path(os.getenv("MODULE_PATH", ".")) / "config/config.json"
OUTPUT_PATH = Path(os.getenv("HOME", "../out"))

# read token from JSON file
SECRETS = json.loads(
    Path(os.getenv("SECRETS_PATH", "../secrets.json")).read_text(encoding="utf-8")
)

# S3 public connection details
ENDPOINT_URL = "https://s3.rbx.io.cloud.ovh.net/"
REGION_NAME = "rbx"


# anonymization function
def anonymization(config_file_path: Path, data_path: Path) -> pd.DataFrame:
    """Anonymization function."""
    config = json.loads(config_file_path.read_bytes())
    df: pd.DataFrame = pd.read_csv(data_path, delimiter=";")
    df_result = anonymize_dataset(df, config)
    return df_result


def get_input_file(file_list: List[FileStorage]) -> Path:
    """Filter and save files sent by the user."""
    DATA: Optional[Path] = None
    for file in file_list:
        splitted_name = file.filename.split(".")
        filename: str = secure_filename(file.filename)
        suffix = splitted_name[len(splitted_name) - 1]

        if suffix == "csv":
            filepath: Path = Path(app.config["UPLOAD_FOLDER"]) / filename
            file.save(filepath)
            DATA = filepath

    if DATA is None:
        raise FileNotFoundError("No CSV file sent")

    return DATA


# -----------------#
#   Flask routes   #
# -----------------#
@app.get("/health")
def health_check():
    """Health check of the application."""
    return Response(status=HTTPStatus.OK)


@app.route("/<customer_id>", methods=["POST"])
@check_token(SECRETS["write_token"])
def push(customer_id: str):
    """Push CSV file to anonymize."""
    if "files" not in request.files:
        return make_response("No file part", 400)
    file_list = request.files.getlist("files")

    if len(file_list) != 1:
        return make_response("Was expecting one file", 400)

    try:
        input_file = get_input_file(file_list)
    except FileNotFoundError as exc:
        return make_response(exc.args[0], 400)

    df_anonymized = anonymization(CONFIG_FILE, input_file)

    # store result in a S3 bucket
    s3 = boto3.resource(
        "s3",
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=SECRETS["aws_access_key_id"],
        aws_secret_access_key=SECRETS["aws_secret_access_key"],
        region_name=REGION_NAME,
    )

    csv = BytesIO(df_anonymized.to_csv(index=False).encode("utf-8"))
    s3.Bucket("mse-s3").upload_fileobj(csv, f"anonymized-data-{customer_id}.csv")

    return make_response(f"{{status: Success, customer_id: {customer_id}}}", 200)


@app.route("/<customer_id>", methods=["GET"])
@check_token(SECRETS["read_token"])
def read(customer_id: str):
    """Retrieve anonymized CSV file."""
    s3 = boto3.resource(
        "s3",
        endpoint_url=ENDPOINT_URL,
        aws_access_key_id=SECRETS["aws_access_key_id"],
        aws_secret_access_key=SECRETS["aws_secret_access_key"],
        region_name=REGION_NAME,
    )

    try:
        csv = s3.Object("mse-s3", f"anonymized-data-{customer_id}.csv").get()

        return send_file(
            BytesIO(csv["Body"].read()),
            as_attachment=True,
            download_name="results.csv",
        )
    except s3.meta.client.exceptions.ClientError:
        return make_response(f"No file found for customer_id: {customer_id}", 400)
