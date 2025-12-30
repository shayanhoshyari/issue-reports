load("@rules_python//python:defs.bzl", "py_binary", "py_test")

py_binary(
    name = "app",
    srcs = ["__main__.py"],
    main = "__main__.py",
    deps = ["//mattress"],
)

py_test(
    name = "app_test",
    srcs = ["__main__.py"],
    main = "__main__.py",
    deps = ["//mattress"],
)
