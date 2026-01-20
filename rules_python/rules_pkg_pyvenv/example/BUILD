load("@rules_pkg_pyvenv//:defs.bzl", "tar_runfiles")
load("@rules_python//python:defs.bzl", "py_binary", "py_test")

py_binary(
    name = "app",
    srcs = ["__main__.py"],
    main = "__main__.py",
    deps = [
        "@pip//cowsay",
    ],
)

tar_runfiles(
    name = "app_tar",
    py_binary = ":app",
)

py_test(
    name = "test_app_tar",
    srcs = ["test_app_tar.py"],
    data = [":app_tar"],
)
