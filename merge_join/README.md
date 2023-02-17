# Merge join for MSE

This demo allows to merge multiple CSV files on a specific column (`siren` in our case).
No one see any CSV file but anyone can see the merge of all CSV files submitted.

## Test locally

It's a good practice before deploying an app into MSE to test it locally:

```console
$ mse test
$ # push your CSV file
$ curl -F "file=@/path/to/csv-file" http://127.0.0.1:5000/
$ # get result of merge on column "siren"
$ curl http://127.0.0.1:5000/
```

## Deploy your application

```console
$ mse deploy  # in same folder as mse.toml
```

Your application is now ready to be used.

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
$ # push your CSV file with your CA bundle
$ curl -F "file=@/path/to/csv-file" https://$APP_DOMAIN_NAME/ --cacert cert.pem
$ # get result of merge on column "siren" with your CA bundle
$ curl https://$APP_DOMAIN_NAME/ --cacert cert.pem
```

See [clients](client/) in various language if you don't want to use `curl`.
