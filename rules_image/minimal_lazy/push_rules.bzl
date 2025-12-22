"""Minimal lazy push style rules used to demonstrate remote cache-only behavior."""

def _producer_impl(ctx):
    """Creates a synthetic blob file.

    The declared output allows Bazel to cache the action remotely. Nothing in
    the downstream graph consumes the bytes, so the cache entry is enough.
    """
    out = ctx.actions.declare_file(ctx.label.name + ".blob")

    ctx.actions.run_shell(
        outputs = [out],
        command = "echo hello > {}".format(out.path),
        mnemonic = "ProduceBlob",
    )

    return DefaultInfo(files = depset([out]))

def _shayan_push_impl(ctx):
    """A rule that depends on `input` but never reads its files.

    Because no action consumes the bytes, Bazel only needs the action cache
    entry for `input` when deciding whether the output exists in the remote
    cache. On a cache hit Bazel will *not* re-execute or download the blob.
    """
    # Depending on the label is enough to put it in the action graph.
    _ = ctx.attr.input

    exe = ctx.actions.declare_file(ctx.label.name)

    ctx.actions.write(
        output = exe,
        content = """#!/bin/sh
echo "Lazy push: relying on remote cache entry for $1"
""",
        is_executable = True,
    )

    return DefaultInfo(
        executable = exe,
        files = depset([exe]),
    )

producer = rule(
    implementation = _producer_impl,
)

shayan_push = rule(
    implementation = _shayan_push_impl,
    attrs = {"input": attr.label(mandatory = True)},
    executable = True,
)
