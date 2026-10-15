# Offline Node bootstrapping demo

This small fixture supports the [Bootstrapping a system](../../knowledge/programming-languages/bootstrapping-a-system.md)
explanation. `app.mjs` imports `learning-greeting` by package name. The package
is a local `file:` dependency, so the install needs no registry download.

To repeat the check, copy this directory to a new disposable location and run
the following commands inside that copy:

```bash
npm start
npm ci --ignore-scripts --offline --no-audit --no-fund
npm start
```

The first `npm start` should fail with `ERR_MODULE_NOT_FOUND`. After the clean
install, it should print `Hello, Ada!`. The committed lockfile must match the
manifest. Keep the fixture's files together when copying it.

On 2026-10-15, Node.js v22.23.2 and npm 10.9.8 produced those two outcomes
in a disposable copy. A second `npm ci` left the lockfile checksum unchanged.
No cloud resource or external service was used. This check does not validate
other Node/npm versions or projects with installation scripts.
