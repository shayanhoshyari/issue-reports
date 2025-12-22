# Minimal lazy-push style example

This directory captures the minimal pattern described in the chat with ChatGPT:

> To ensure a target's outputs exist in remote cache without forcing a download,
> depend on the producing action but never consume its output files.

## Layout

* `push_rules.bzl` — defines two rules:
  * `producer`: creates a cacheable blob via a shell action.
  * `shayan_push`: executable rule that depends on `producer` but does not read
    its outputs, mirroring `rules_img`'s lazy push behaviour.
* `BUILD.bazel` — wires the two rules together (`:layer` and `:push`).
* `.bazelrc` — pins the requested cache, Python, and `__init__.py` settings.
* `bazel` — wrapper script that downloads Bazelisk on demand and proxies
  invocations.

## How to try it

```bash
cd rules_image/minimal_lazy
./bazel build //:push \
  --remote_download_outputs=minimal
```

Notes:

1. The wrapper caches Bazelisk in `${XDG_CACHE_HOME:-$HOME/.cache}/ai_platform`.
2. The `.bazelrc` sets a default gRPC remote cache; override it locally if you
   don't have access, e.g. `./bazel build //:push --remote_cache=file://$PWD/.remote-cache`.
3. On a cache hit, Bazel records the output digest for `:layer` but does **not**
   download `layer.blob` because nothing depends on the file contents.
