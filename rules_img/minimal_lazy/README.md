# Minimal lazy-push example

An example to show how we can leverage bazel build to only build sth if it does not already exist in remote cache, and otherwise, never materialize on disk.

## Layout

* `push_rules.bzl` — defines two rules:
  * `producer`: creates a cacheable blob via a shell action.
  * `shayan_push`: executable rule that depends on `producer` but does not read
    its outputs, mirroring `rules_img`'s lazy push behaviour.
* `BUILD.bazel` — Uses two rules (`:layer` and `:push`).
* `.bazelrc` — pins the requested cache, Python, and `__init__.py` settings.
* `bazel` — wrapper script that downloads Bazelisk on demand and proxies
  invocations.

## How to try it

```bash
cd rules_image/minimal_lazy
./bazel build //:push
```

**Expected behavior**: On a cache hit, Bazel records the output digest for `:layer` but does **not**
  download `layer.blob` because nothing depends on the file contents. When there is not cache hit, it builds it and uploads it to the remote cache.
