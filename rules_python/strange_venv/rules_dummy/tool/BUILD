load("@rules_python//python:defs.bzl", "py_binary")

py_binary(
    name = "tool",
    srcs = ["__main__.py"],
    main = "__main__.py",
    visibility = ["//visibility:private"],
    deps = [
        "@pip//cowsay",
        "@pip//google_cloud_storage",
    ],
)
