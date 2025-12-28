load("@rules_python//python:defs.bzl", "py_library")

# When this is included in a py_binary (through --@rules_python//python/config_settings:debugger=//.vscode/debugpy:attach)
# it will make the root process to attach to running debugpy.
py_library(
    name = "attach",
    srcs = ["sitecustomize.py"],
    imports = ["."],
    visibility = ["//:__subpackages__"],
)