# MSE App Demo

You can find several app demos runnable in a MSE architecture.

Each example contains:
- A file `mse.toml` which is the configuration of the MSE app.
- A folder `code` which is the code to run inside the MSE node.
- A folder `test` which enables you to unittest your application locally or remotly.

These examples have been generated using:

```console
$ mse-ctl scaffold $NAME
```

You can test locally this app doing:

```console
$ mse-ctl test
$ # From another terminal:
$ pytest
```

You can quickly deploy this app doing:

```console
$ mse-ctl deploy --path demo_name/mse.toml
```

And test it:

```console
$ TEST_REMOTE_URL="https://<app_domain_name>" pytest
```

## Demo list

|                               Name                               |         SSL Certificate origin         |
| :--------------------------------------------------------------: | :------------------------------------: |
|                [helloworld](helloworld/README.md)                | Self (enclave)  or  Operator (Cosmian) |
|             [float average](float_average/README.md)             |             Self (enclave)             |
| [float average trust owner](float_average_trust_owner/README.md) |               App Owner                |
|                [merge join](merge_join/README.md)                |             Self (enclave)             |

## Annexes

Here a way to tar an example to be run inside `mse-docker`:

```console
$ tar -cvf $PWD/helloworld.tar --directory=helloworld/code app.py requirements.txt
```
