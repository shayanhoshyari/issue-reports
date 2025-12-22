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
* `WORKSPACE.bazel` — declares a standalone workspace so you can `bazel build`
  from this folder.

## How to try it

Use any remote cache endpoint; a local file-based cache is enough to demonstrate
behaviour:

```bash
cd rules_image/minimal_lazy
bazelisk build //:push \
  --remote_cache=file://$PWD/.remote-cache \
  --remote_upload_local_results=true \
  --remote_download_outputs=minimal
```

What happens:

1. On the first build Bazel executes `producer`, uploads `layer.blob`, and builds
   the tiny `:push` executable.
2. On a clean tree hitting the same cache, Bazel finds the `producer` action in
   the remote cache, records the digest, **does not download** `layer.blob`, and
   rebuilds only the small `:push` file.

This matches the guidance from the conversation: as long as no downstream action
calls `ctx.files.input` (or similar), Bazel only needs the action cache metadata
and will not fetch the blob bytes from remote storage.
