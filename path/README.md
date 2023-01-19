# Path

Basic example of how to use dedicated path in a mse application.

 This example works with a self-signed certificate on a fully zero trust environment and containing:
- A simple helloworld flask application
- The mse app config file
- A secret file
- Python tests

## Test it locally

On a first terminal, run:

```console
$ # From path directory
$ cd mse_src
$ SECRETS_PATH=../secrets.json flask run
```

You can also run instead: 

```console
$ # From path directory
$ mse test
```

On a second terminal, run:

```console
$ # From path directory
$ rm -f $HOME/date.txt
$ pytest
```

## Deploy your application

```console
$ mse deploy 
```

Your application is now ready to be used

## Test it

```console
$ TEST_REMOTE_URL="https://<app_domain_name>" pytest
```

## Use it 


You can get the certificate and check it using:

```console
$ mse verify --skip-fingerprint "<uuid.cosmian.app>"
```

You can now query the microservice:

```sh
$ curl https://<uuid.cosmian.app>/ --cacert cert.pem
```