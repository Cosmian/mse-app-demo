# Path

Basic example of how to use dedicated paths in an mse application.

 This example works with a self-signed certificate on a fully zero trust environment. This example contains:

- A simple hello-world flask application
- The mse app config file
- A secret file
- Python tests

## Test it locally

On a first terminal, run:

```console
$ # From `path` example directory
$ cd mse_src
$ SECRETS_PATH=../secrets.json flask run
```

You can also run instead:

```console
$ # From `path` example directory
$ mse test
```

On a second terminal, run:

```console
$ # From `path` example directory
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
$ TEST_REMOTE_URL="https://<uuid.cosmian.app>" pytest
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

### Authentication using tokens

The file `secrets.json` contains the tokens used by the app to manage authentication.
In a real-world application, this file should not be pushed on a public git repository.

Write current date into file

```sh
$ curl -H "Authorization: Bearer 6fMvPktkMwZj5UJwxasOIj7sO37H4DfZZo05Nn1fFYw=" -X POST https://<uuid.cosmian.app>/ --cacert cert.pem
```

Read the date file

```sh
$ curl -H "Authorization: Bearer bAyJhel6vwzrvNcy7ux2nULRwpP6BviE34KSiZRGixo=" https://<uuid.cosmian.app>/ --cacert cert.pem
```
