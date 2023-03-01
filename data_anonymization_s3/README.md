# Data Anonymization with storage using S3

Example of a mse application to anonymize data and store the result in a bucket S3.

This example works with a self-signed certificate on a fully zero trust environment and contains:

- a simple flask API
- 2 client scripts, a data provider and a data consumer
- Python tests
- an example dataset to anonymize with the right configuration file associated

To use your own dataset, your data must be a csv file with comma or semi-colon separator. Encoding must be UTF-8.

The configuration file (.json) must be generated with [Cosmian Anonymization tool](https://hub.docker.com/r/cosmian/anonymization_ui).

## Setup

Create an AWS S3 storage and edit the connection information in `mse_src/app.py` and `secrets.json`.

## Deploy your application

```console
$ mse deploy 
```

Your application is now ready to be used

## Test it

```console
$ TEST_REMOTE_URL="https://$APP_DOMAIN_NAME" pytest
```

## Use it

You can get the certificate and check it using:

```console
$ mse verify "$APP_DOMAIN_NAME"
```

### Upload the data to anonymize

In `untrusted ssl` mode:

```sh
$ python clients/data_provider.py "https://$APP_DOMAIN_NAME"
```

Or in `zero trust` mode:

```sh
$ python clients/data_provider.py "https://$APP_DOMAIN_NAME" --ssl
```

### Get the anonymized data

In `untrusted ssl` mode:

```sh
$ python clients/data_consumer.py "https://$APP_DOMAIN_NAME"
```

Or in `zero trust` mode:

```sh
$ python clients/data_consumer.py "https://$APP_DOMAIN_NAME" --ssl
```
