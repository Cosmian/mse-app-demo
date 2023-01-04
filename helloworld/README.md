# Helloworld

Basic example of an mse application containing:
- A simple helloworld flask application
- The mse app config file

Two configurations are availables: 
- `config/dev.toml`: work on dev mode which means with a cosmian certificate
- `config/zero_trust.toml`: work with a self-signed certificate on a fully zero trust environment

## Deploy your application

```console
$ mse-ctl deploy --path config/zero_trust.toml
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
$ mse-ctl verify --skip-fingerprint "<uuid.cosmian.app>"
```

You can now query the microservice:

```sh
$ curl https://<uuid.cosmian.app>/ --cacert cert.pem
```