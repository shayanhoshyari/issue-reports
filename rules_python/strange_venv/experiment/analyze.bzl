
def _analyze_pybinary_impl(ctx):
    binary = ctx.attr.target
    runfiles = binary[DefaultInfo].default_runfiles

    debug_data = []

    # Capture the runfiles
    # for file in runfiles.files.to_list():
    #     debug_data.append("File: {} {} {}".format(file.is_symlink, file.short_path, file.path))

    for symlink in runfiles.symlinks.to_list():
        debug_data.append("SymlinkEntry: {} -> {}".format(symlink.path, symlink.target_file))

    for symlink in runfiles.root_symlinks.to_list():
        debug_data.append("RootSymlinkEntry: {} -> {}".format(symlink.path, symlink.target_file))

    out = ctx.actions.declare_file(ctx.label.name + ".txt")
    ctx.actions.write(
        output = out,
        content = "\n".join(debug_data),
    )

    return [DefaultInfo(files = depset([out]))]

analyze_pybinary = rule(
    implementation = _analyze_pybinary_impl,
    attrs = {
        "target": attr.label(mandatory = True),
    },
    doc = "Run various debug analysis on a given py_binary target to see where the bug is coming form.",
)
