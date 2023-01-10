# Helloworld

Basic example of an mse application working with a self-signed certificate on a fully zero trust environment and containing:
- A simple helloworld flask application
- The mse app config file

## Deploy your application

```console
$ mse deploy --path mse.toml
```

Your application is now ready to be used

## Test it

```console
$ TEST_REMOTE_URL="https://<app_domain_name>" pytest
```

## Use it 

### Deployment using dev.toml

```sh
$ curl https://<uuid.cosmian.dev>/
```

### Deployment using zero_trust.toml

You can get the certificate and check it using:

```console
$ mse verify --skip-fingerprint "<uuid.cosmian.app>"
```

You can now query the microservice:

```sh
$ curl https://<uuid.cosmian.app>/ --cacert cert.pem
```