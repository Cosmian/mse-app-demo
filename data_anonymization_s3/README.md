# Data Anonymization

Example of a mse applications to anonymize data.

This example works with a self-signed certificate on a fully zero trust environment and contains:

- a simple flask API
- 2 client scripts, a data provider and a data consumer
- Python tests
- an example dataset to anonymize with the right configuration file associated

To use your own dataset, your data must be a csv file with comma or semi-colon separator. Encoding must be UTF-8.

The configuration file (.json) must be generated with [Cosmian Anonymization tool](https://hub.docker.com/r/cosmian/anonymization_ui).

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

You can now upload the data to anonymize:

```sh
$ python3 clients/data_provider.py $APP_DOMAIN_NAME [--ssl]
```

And finally get the anonymized data:

```sh
$ python3 clients/data_consumer.py $APP_DOMAIN_NAME [--ssl]
```
