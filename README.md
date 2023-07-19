# MSE App Examples

You can find several app examples runnable in a MSE architecture.

Each example contains:
- A file `mse.toml` which is the configuration of the MSE app.
- A folder `mse_src` which is the code to run inside the MSE node.
- A folder `test` which enables you to unittest your application locally or remotly.

You can read the full [documentation](https://docs.cosmian.com/microservice_encryption/getting_started/) for more details about MSE and `mse-cli`.

Clone the repository as follow: 

```console
# apt install git-lfs
$ git clone https://github.com/Cosmian/mse-app-examples
```

These examples have been generated using:

```console
$ mse cloud scaffold $NAME
```

You can test locally an app doing:

```console
$ cd example_name
$ mse cloud localtest
```

You can quickly deploy this app doing:

```console
$ cd example_name
$ mse cloud deploy
```

And test it:

```console
$ mse cloud test <APP_ID>
```

## Examples list

|                                    Name                                     |                                                         Usage scenario                                                          |
| :-------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------: |
|                     [helloworld](helloworld/README.md)                      | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |
|             [fastapi-helloworld](fastapi_helloworld/README.md)              | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |
|                     [merge join](merge_join/README.md)                      | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |
|                           [path](path/README.md)                            | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |
|              [yaos millionaires](yaos_millionaires/README.md)               | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |
|  [yaos millionaires trust owner](yaos_millionaires_trust_owner/README.md)   |     [App Owner trusted](https://docs.cosmian.com/microservice_encryption/scenarios/#app-owner-trusted-fully-encrypted-saas)     |
|          [data_anonymization_s3](data_anonymization_s3/README.md)           | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |
|        [digit recognition (tensorflow)](digit_recognition/README.md)        | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |
| [sentiment analysis (pytorch & transformers)](sentiment_analysis/README.md) | [Zero Trust](https://docs.cosmian.com/microservice_encryption/scenarios/#zero-trust-collaborative-confidential-computation-ccc) |

## Dockers list

This repository also provides some allowed mse dockers. See [the packages](https://github.com/orgs/Cosmian/packages?repo_name=mse-app-examples) to get the up-to-date references. The dockerfile are written in these following examples:

|       Name        |                        Dockerfile                         |
| :---------------: | :-------------------------------------------------------: |
| mse-anonymization | [data_anonymization_s3](data_anonymization_s3/Dockerfile) |
|      mse-ds       |            [merge_join](merge_join/Dockerfile)            |
|    mse-fastapi    |    [fastapi_helloworld](fastapi_helloworld/Dockerfile)    |
|     mse-flask     |            [helloworld](helloworld/Dockerfile)            |
|      mse-nlp      |    [sentiment_analysis](sentiment_analysis/Dockerfile)    |
|  mse-tensorflow   |     [digit_recognition](digit_recognition/Dockerfile)     |

## Annexes

Here a way to tar an example to be run inside an [mse-docker](https://github.com/Cosmian/mse-docker-base):

```console
$ tar -cvf $PWD/helloworld.tar --directory=helloworld/mse_src app.py requirements.txt
```
