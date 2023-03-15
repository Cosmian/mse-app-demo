# Yao's millionaires for MSE

This example allows to share integers and get the position of the maximum added interger.
No one see the set of integers, only the position of the user who added the highest number is known.

## Test locally

It's a good practice before deploying an app into MSE to test it locally:

```console
$ mse test
$ # push an integer
$ curl -X POST -H 'Content-Type: application/json' -d '{"n": 2.5}' http://127.0.0.1:5000/
$ # get the position of the user who added the maximum value
$ curl http://127.0.0.1:5000/
```

## Deploy your application

```console
$ mse deploy  # in same folder as mse.toml
```

Your application is now ready to be used.

## Test it

```console
$ TEST_REMOTE_URL="https://$APP_DOMAIN_NAME" pytest
```

## Use it

Get the SSL certificate (without checking the trustworthiness of the enclave):

```console
$ # replace $APP_DOMAIN_NAME with your own app domaine name
$ openssl s_client -showcerts -connect $APP_DOMAIN_NAME:443 </dev/null 2>/dev/null | openssl x509 -outform PEM > cert.pem
```

check that it runs in an Intel SGX enclave (not checking code fingerprint):

```console
$ mse verify $APP_DOMAIN_NAME
```

then just query your trusted microservice:

```console
$ # push an integer with your CA bundle
$ curl -X POST -H 'Content-Type: application/json' -d '{"n": 2.5}' https://$APP_DOMAIN_NAME/ --cacert cert.pem
$ # get the user with the max value with your CA bundle
$ curl https://$APP_DOMAIN_NAME/ --cacert cert.pem
```

See [clients](client/) in various language if you don't want to use `curl`.
