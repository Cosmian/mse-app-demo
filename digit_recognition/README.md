# Digit recognition for MSE

The aim of this example is to provide an app to perform digit recognition from a drawn canvas, based on a trained model, using `tensorflow` and `keras`.

## Deploy your application

```console
$ mse cloud deploy  # in same folder as mse.toml
```

Your application is now ready to be used.

## Test it

```console
$ mse cloud test <APP_ID>
```

## Use it

### With gradio

Using gradio, you can run locally the given gradio interface :
```console
$ pip install gradio
$ gradio client/client.py
```

And access the interface at the given local url.


### Using curl

Get the SSL certificate (without checking the trustworthiness of the enclave):

```console
$ # replace $APP_DOMAIN_NAME with your own app domaine name
$ openssl s_client -showcerts -connect $APP_DOMAIN_NAME:443 </dev/null 2>/dev/null | openssl x509 -outform PEM > cert.pem
```

You can also get the certificate and check it using:

```console
$ mse cloud verify "$APP_DOMAIN_NAME"
```

then just query your trusted microservice with the given client:

```console
$ # launch local python server
$ python client/server.py
$ # open html page, provide the domain name of your deployed app, and draw a digit
```
