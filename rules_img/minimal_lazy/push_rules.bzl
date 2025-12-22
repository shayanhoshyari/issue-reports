"""Minimal lazy push style rules used to demonstrate remote cache-only behavior."""

def _producer_impl(ctx):
    """Creates a synthetic blob file.

    The declared output allows Bazel to cache the action remotely. Nothing in
    the downstream graph consumes the bytes, so the cache entry is enough.
    """
    out = ctx.actions.declare_file(ctx.label.name + ".blob")

    ctx.actions.run_shell(
        outputs = [out],
        command = "sleep 3 && dd if=/dev/zero of={} bs=1M count=1024".format(out.path),
        mnemonic = "ProduceBlob",
    )

    return DefaultInfo(files = depset([out]))

def _shayan_push_impl(ctx):
    """A rule that depends on `input`.
    The goal of this rule is: Ensure input exits in remote cache
    1. If input does not exist in remote cache, it builds it and uploads it
    2. otherwise, it does not build or even download it.
    """
    input = ctx.file.input

    exe = ctx.actions.declare_file(ctx.label.name)

    # This is the secret sauce:
    # 1. don't add input to DefaultInfo
    # 2. Add a file to DefaultInfo (here exe), that needs input to be produced.
    #
    # It works because the final goal is to get exe, so if exe is in remote cache, input should
    # not be materialized. In reality bazel is checking if exe is in remote cache, and not input
    # :)
    ctx.actions.run_shell(
        inputs = [input],
        outputs = [exe],
        command = """
INPUT_SIZE=$(du -h $(realpath {0}) | awk '{{print $1}}')
cat > {1} << EOF
#!/bin/sh
echo "Lazy push: relying on remote cache entry"
echo "My input was \"$INPUT_SIZE bytes\""
EOF
chmod +x {1}
""".format(input.path, exe.path),
        mnemonic = "CreatePushScript",
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
    attrs = {"input": attr.label(mandatory = True, allow_single_file = True)},
    executable = True,
)
