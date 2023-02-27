# Digit recognition with trusted owner

The aim of this demo is to provide an app to do digit recognition from a drawn canva, based on a trained model, using tensorflow and keras.
In this example we use a custom certificate provided by the app owner.
It means that the TLS connection is controlled by the application owner instead of being generated directly in the enclave.

In that scenario, the app owner provides the SSL certificate related to its domain name:

```toml
[certificate]
private_key="key.pem"
certificate="cert.pem"
domain_name="demo.owner.app"
```

You need a valid certificate signed by a trust authority if you want your microservice to work in web browsers.

As an example, you can use ACME protocol and DNS-01 method with Let's Encrypt to get a trusted certificate:

```console
$ sudo certbot certonly --dns-ovh --dns-ovh-credentials ovhapi.conf -d demo.owner.app -m tech@owner.com -n --agree-tos
```

Also add a new `CNAME` record in your DNS registry for `demo.owner.app` to `proxy.cosmian.com` prior to the app deployment.
This domain name will be used for `mse deploy`.

## Deploy your application

```console
$ mse deploy
```

Your application is now ready to be used.

## Test it

```console
$ TEST_REMOTE_URL="https://$APP_DOMAIN_NAME" pytest
```

## Use it

You can now query the app from JavaScript your web browser.

Try with `client/index.html`.
