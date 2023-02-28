# MSE App Examples

You can find several app examples runnable in a MSE architecture.

Each example contains:
- A file `mse.toml` which is the configuration of the MSE app.
- A folder `mse_src` which is the code to run inside the MSE node.
- A folder `test` which enables you to unittest your application locally or remotly.

You can read the full [documentation](https://docs.cosmian.com/microservice_encryption/getting_started/) for more details about MSE and `mse-cli`.

These examples have been generated using:

```console
$ mse scaffold $NAME
```

You can test locally an app doing:

```console
$ cd example_name
$ mse test
$ # From another terminal:
$ cd example_name
$ pytest
```

You can quickly deploy this app doing:

```console
$ cd example_name
$ mse deploy
```

And test it:

```console
$ cd example_name
$ TEST_REMOTE_URL="https://<app_domain_name>" pytest
```

## Examples list

|                                   Name                                   |                                                         Usage scenario                                                          |
| :----------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------: |
|                    [helloworld](helloworld/README.md)                    | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |
|            [fastapi-helloworld](fastapi_helloworld/README.md)            | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |
|                    [merge join](merge_join/README.md)                    | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |
|                          [path](path/README.md)                          | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |
|             [yaos millionaires](yaos_millionaires/README.md)             | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |
| [yaos millionaires trust owner](yaos_millionaires_trust_owner/README.md) |     [App Owner trusted](https://docs.cosmian.com/microservice_encryption/scenarios/#app-owner-trusted-fully-encrypted-saas)     |
| [digit recognition trust owner](digit_recognition_trust_owner/README.md) |     [App Owner trusted](https://docs.cosmian.com/microservice_encryption/scenarios/#app-owner-trusted-fully-encrypted-saas)     |
|         [data_anonymization_s3](data_anonymization_s3/README.md)         | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |

## Annexes

Here a way to tar an example to be run inside an [mse-docker](https://github.com/Cosmian/mse-docker-base):

```console
$ tar -cvf $PWD/helloworld.tar --directory=helloworld/mse_src app.py requirements.txt
```
