"""Gradio interface to play with digit recognition example"""
import base64
import io
import json
import subprocess

import gradio as gr
import requests
from PIL import Image


def update_domain_name(domain):
    """Function to update second domain name input according to the first one"""
    return {domain_name2: gr.update(value=domain)}


def verify(domain):
    """Function to run mse app verification"""
    with subprocess.Popen(["mse", "verify", domain], stdout=subprocess.PIPE) as process:
        text = (
            process.stdout.read()
            .decode("utf-8")
            .replace("[93m", "")
            .replace("[0m", "\n")
            .replace("[92m", "")
        )
        return {text_informs: gr.update(value=text)}


def predict_digit(domain, cert_path, data):
    """Function to query the app recognition"""
    img = Image.fromarray(data)

    buffer = io.BytesIO()
    img.save(buffer, format="JPEG")
    base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
    image = "data:image/png;base64," + base64_image
    certificate = cert_path if cert_path else False
    response = requests.post(
        f"https://{domain}/", json={"data": image}, verify=certificate
    )
    response_json = json.loads(response.content)
    return response_json["number"]


with gr.Blocks() as demo:
    gr.Markdown("# Encrypted Digit Recognition\n")
    gr.Markdown(
        "MicroService Encryption (MSE) allows to easily deploy confidential web application written in Python in Cosmian’s infrastructure with the following security features:\n- Code runs in a Trusted Execution Environment (TEE) and is encrypted with your own key.\n- Secure channel is established directly and uniquely with your code in the TEE.\n- Everyone interacting with your microservice can verify that your code runs in a TEE thanks to a Transport Layer Security (TLS) extension called Remote Attestation TLS (RA-TLS).\n"
    )

    gr.Markdown(
        "**This demo performs a digit recognition using a trained model deployed as a microservice.**"
    )
    gr.Markdown(
        "*Please make sure that you have deployed you own digit recognition application using digit_recognition MSE's example and mse CLI, or that you have the domain name of this deployed example and mse CLI installed.*"
    )
    gr.Image(
        label="Usage flow",
        value="https://docs.cosmian.com/microservice_encryption/images/use-app-owner-trust.png",
    )

    gr.Markdown(
        "In Zero trust approach the user has to verify the MSE app and the SSL certificate before querying the app. The following diagram explains how it works:"
    )
    gr.Image(
        label="Usage flow",
        value="https://docs.cosmian.com/microservice_encryption/images/use.png",
    ).style(height=400)

    gr.Markdown("## 1 | Microservice Encryption instance verification\n")
    gr.Markdown(
        "The app user should verify the MSE app, that is to say:\n- check that the code is running inside an enclave\n- check that this enclave belongs to Cosmian\n- check that the code is exactly the same as provided by the app owner\nIf one of those fails, the app owner must stop querying the application."
    )
    with gr.Row():
        domain_name = gr.Textbox(label="Domain name")
        text_informs = gr.Markdown(value="")
    verify_button = gr.Button("Verify the microservice")

    gr.Markdown("## 2 | Microservice querying\n")
    gr.Markdown(
        "The app user can now query the running microservice with the given path certificate:"
    )
    with gr.Row():
        canva = gr.Sketchpad().style(height=280, width=280)
        with gr.Column():
            domain_name2 = gr.Textbox(label="Domain name", value=domain_name.value)
            path = gr.Textbox(label="Path to ceritificate")
            digit = gr.Textbox(label="Digit")
    button_classify = gr.Button("Send digit")

    domain_name.change(
        fn=update_domain_name, inputs=[domain_name], outputs=[domain_name2]
    )
    verify_button.click(fn=verify, inputs=[domain_name], outputs=[text_informs])

    button_classify.click(
        fn=predict_digit,
        inputs=[domain_name, path, canva],
        outputs=[digit],
    )

demo.launch()
