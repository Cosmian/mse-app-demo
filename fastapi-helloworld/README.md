# FastAPI: Helloworld

Basic example of an mse application working with a self-signed certificate on a fully zero trust environment and containing:

- A simple helloworld fastAPI application
- The mse app config file

***WARNING***: the command `mse test` is currently not working for fastAPI.

## Deploy your application

```console
$ mse deploy 
```

Your application is now ready to be used

## Use it

You can get the certificate and check it using:

```console
$ mse verify --skip-fingerprint $APP_DOMAIN_NAME
```

You can now query the microservice:

```sh
$ curl https://$APP_DOMAIN_NAME/ --cacert cert.pem
```