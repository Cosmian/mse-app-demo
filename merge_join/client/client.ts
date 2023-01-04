/* Simple TypeScript client for merge_join microservice.

```console
$ deno run --allow-net --allow-read --allow-write client.ts http://127.0.0.1:5000  # for local testing
```

If you want to test with MSE:

```console
$ # write SGX self-signed certificate to /tmp
$ openssl s_client -showcerts -connect XXX.cosmian.app:443 </dev/null 2>/dev/null | openssl x509 -outform PEM >/tmp/cert.pem
$ # install intel-sgx-ra to do remote attestation
$ pip3 install intel-sgx-ra
$ sgx-ra-verify certificate --path /tmp/cert.pem  # SGX Remote Attestation
$ # run with self-signed certificate as CA bundle
$ deno run --cert /tmp/cert.pem --allow-net --allow-read --allow-write client.ts https://XXX.cosmian.app
```

*/

import { basename, resolve } from "https://deno.land/std@0.165.0/path/posix.ts";

async function reset(url: string) {
  const response = await fetch(url, { method: "DELETE" });

  if (response.status != 200) {
    throw new Error(`Bad response: ${response.status}`);
  }
}

async function push(url: string, filePath: string) {
  const fileName = basename(filePath);
  const f = await Deno.readFile(filePath);
  const file = new File([f], fileName);
  const form = new FormData();
  
  form.append("file", file, fileName);

  const response = await fetch(url, {
    method: "POST",
    body: form,
  });

  if (response.status != 200) {
    throw new Error(`Bad response: ${response.status}`);
  }
}

async function merge(url: string): Promise<Blob> {
  const response = await fetch(url);

  if (response.status != 200) {
    throw new Error(`Bad response: ${response.status}`);
  }

  return response.blob();
}

// main
const url: string = Deno.args[0];

await reset(url);

const dataPath = "data/";

for await (const dirEntry of Deno.readDir(dataPath)) {
  await push(url, resolve(dataPath, dirEntry.name));
}

const blob = await merge(url);
await Deno.writeFile("result.csv", new Uint8Array(await blob.arrayBuffer()));
