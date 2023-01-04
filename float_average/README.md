# Float average for MSE

This demo allows to share integers and get the average on them.
No one see the set of integers, only the average and the number of submission is known.

## Test locally

It's a good practice before deploying an app into MSE to test it locally:

```console
$ mse-ctl test
$ # push an integer
$ curl -X POST -H 'Content-Type: application/json' -d '{"n": 2.5}' http://127.0.0.1:5000/
$ # get the statistical mean
$ curl http://127.0.0.1:5000/
```

## Deploy your application

```console
$ mse-ctl deploy  # in same folder as mse.toml
```

Your application is now ready to be used.

## Test it

```console
$ TEST_REMOTE_URL="https://<app_domain_name>" pytest
```

## Use it

Get the SSL certificate (without checking the trustworthiness of the enclave):

```console
$ # replace with your <uuid>
$ openssl s_client -showcerts -connect <uuid>.cosmian.app:443 </dev/null 2>/dev/null | openssl x509 -outform PEM > cert.pem
```

check that it runs in an Intel SGX enclave (not checking code fingerprint):

```console
$ mse-ctl verify --skip-fingerprint <uuid>.cosmian.app
```

then just query your trusted microservice:

```console
$ # push an integer with your CA bundle
$ curl -X POST -H 'Content-Type: application/json' -d '{"n": 2.5}' https://<uuid>.cosmian.app/ --cacert cert.pem
$ # get the statistical mean with your CA bundle
$ curl https://<uuid>.cosmian.app/ --cacert cert.pem
```

See [clients](client/) in various language if you don't want to use `curl`.
