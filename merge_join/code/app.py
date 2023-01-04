"""app module."""

from http import HTTPStatus
from io import BytesIO
import logging
from pathlib import Path
from typing import Iterator, Any

from flask import Flask, Response, request, send_file
import pandas as pd
from werkzeug.utils import secure_filename

import globs


SEP: str = ";"

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "/tmp"

logging.basicConfig(format="[%(levelname)s] %(message)s", level=logging.DEBUG)


def merge_all(datas: Iterator[Path], on: str) -> pd.DataFrame:
    """Inner join of CSV files in `datas`."""
    dataframe: pd.DataFrame

    try:
        dataframe = pd.read_csv(next(datas), sep=SEP)
    except StopIteration as exc:
        raise Exception("No input data!") from exc

    for data in datas:  # type: Path
        dataframe = pd.merge(
            dataframe,
            pd.read_csv(data, sep=SEP),
            how="inner",
            on=on,
        )

    return dataframe


@app.get("/health")
def health_check():
    """Health check of the application."""
    return Response(status=HTTPStatus.OK)


@app.post("/")
def push():
    """Push CSV file for future merge."""
    if "file" not in request.files:
        app.logger.error("No file part")
        return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)

    file = request.files["file"]

    if not file or file.filename == "":
        app.logger.error("No file")
        return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)

    filename: str = secure_filename(file.filename)
    filepath: Path = Path(app.config["UPLOAD_FOLDER"]) / filename
    
    if filepath.suffix == ".csv":
        file.save(filepath)

        globs.CSVS.append(filepath)

        app.logger.info("Successfully added %s", filename)
        return Response(status=HTTPStatus.OK)

    app.logger.error("Not a CSV file")

    return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)


@app.get("/")
def merge():
    """Merge all CSVs uploaded."""
    if len(globs.CSVS) < 2:
        app.logger.error("need more than 2 CSVs to merge")
        return Response(status=HTTPStatus.UNPROCESSABLE_ENTITY)

    result: pd.DataFrame = merge_all(iter(globs.CSVS), "siren")

    return send_file(
        BytesIO(result.to_csv(index=False, sep=SEP).encode("utf-8")),
        mimetype="text/csv",
        as_attachment=True,
        download_name="result.csv",
    )


@app.delete("/")
def reset():
    """Reset CSV files."""
    for path in globs.CSVS:
        app.logger.info(f"Removed '{path.name}'")
        path.unlink()

    globs.CSVS = []

    app.logger.info("Reset successfully")

    return Response(status=HTTPStatus.OK)
