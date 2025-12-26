load("@rules_python//python:defs.bzl", "py_library")

# This variant uses venv and pth
py_library(
    name = "venv",
    srcs = [
        "site-packages/_attach_debugpy.py"
    ],
    data = [
        "site-packages/attach_debugpy.pth"
    ],
    # Why? It seems just "site-packages" does not work, and I need the package_name()
    # Found this out from https://github.com/bazel-contrib/rules_python/blob/a94bd0fdde426bf30efed7c819422d74b404cc18/tests/venv_site_packages_libs/ext_with_libs/BUILD.bazel#L92
    imports = [package_name() + "/site-packages"],
    visibility = ["//:__subpackages__"],
    # This is not meant for public use, but for sake of making a reproducer we use it here.
    experimental_venvs_site_packages = "@rules_python//python/config_settings:venvs_site_packages",
)

# This variant uses imports and sitecustomize
py_library(
    name = "imports",
    srcs = ["sitecustomize.py"],
    imports = ["."],
    visibility = ["//:__subpackages__"],
)