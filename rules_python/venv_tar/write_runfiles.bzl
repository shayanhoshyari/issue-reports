load("@rules_python//python:defs.bzl", "PyRuntimeInfo")

def _write_runfiles(ctx):
    py_binary = ctx.attr.py_binary

    # 1. Write the runfiles
    output = []
    default_info = py_binary[DefaultInfo]

    for f in default_info.default_runfiles.files.to_list():
        if f.path.startswith("external/"):
            # Skip the external ones for easier reading
            continue
        line = "- {}\n- {}\n- {}\n".format(f.path, f.short_path, f.is_symlink)
        output.append(line)

    manifest = ctx.actions.declare_file(ctx.attr.name + ".txt")
    ctx.actions.write(
        output = manifest,
        content = "\n".join(output),
    )

    return [
        DefaultInfo(files = depset([manifest])),
    ]

write_runfiles = rule(
    implementation = _write_runfiles,
    attrs = {
        "py_binary": attr.label(
            doc = "py_binary target whose runfiles to iterate over.",
            providers = [PyRuntimeInfo],
        ),
    },
    doc = "A rule that writes the runfiles of a py_binary to a manifest file.",
)
