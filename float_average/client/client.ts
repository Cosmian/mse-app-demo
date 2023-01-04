/* Simple TypeScript client for float_average microservice.

```console
$ deno run --allow-net client.ts http://127.0.0.1:5000  # for local testing
```

If you want to test with MSE:

```console
$ # write SGX self-signed certificate to /tmp
$ openssl s_client -showcerts -connect XXX.cosmian.app:443 </dev/null 2>/dev/null | openssl x509 -outform PEM >/tmp/cert.pem
$ # install intel-sgx-ra to do remote attestation
$ pip3 install intel-sgx-ra
$ sgx-ra-verify certificate --path /tmp/cert.pem  # SGX Remote Attestation
$ # run with self-signed certificate as CA bundle
$ deno run --cert /tmp/cert.pem --allow-net client.ts https://XXX.cosmian.app
```

*/

interface Mean {
    readonly count: number,
    readonly mean: number
}

async function reset(url: string) {
  const response = await fetch(url, { method: "DELETE" });

  if (response.status != 200) {
    throw new Error(`Bad response: ${response.status}`);
  }
}

async function push(url: string, n: number) {
  const response = await fetch(url, {
    method: "POST",
    body: JSON.stringify({ "n": n }),
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (response.status != 200) {
    throw new Error(`Bad response: ${response.status}`);
  }
}

async function mean(url: string): Promise<Mean> {
  const response = await fetch(url);

  if (response.status != 200) {
    throw new Error(`Bad response: ${response.status}`);
  }

  return response.json();
}

// main
const numbers: Array<number> = [110_000, 25_000, 55_000];

const url: string = Deno.args[0];

await reset(url);

for (const n of numbers) {
  await push(url, n);
}

console.log(await mean(url));
