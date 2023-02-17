from http import HTTPStatus

from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/health")
def health_check():
    """Health check of the application."""
    return Response(status_code=HTTPStatus.OK)


@app.get("/")
def hello():
    """Get a simple example."""
    return "Hello world"
