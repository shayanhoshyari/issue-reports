load("@rules_python//python:defs.bzl", "py_binary", "py_test")


py_binary(
    name = "app",
    srcs = [
        "__main__.py"
    ],
    main = "__main__.py",
    deps = [
        "//mattress",
    ],
)

py_test(
    name = "app_test",
    srcs = [
        "__main__.py"
    ],
    main = "__main__.py",
    deps = [
        "//mattress",
    ],
)


# There is a bug with rules_python that does not propagate imports
# for the added lib. So I have to put site customize here for now.
py_library(
    name = "debugpy",
    srcs = ["sitecustomize.py"],
    visibility = ["//:__subpackages__"],
)