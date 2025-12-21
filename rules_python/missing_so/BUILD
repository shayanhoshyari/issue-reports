load("@rules_python//python:defs.bzl", "py_binary")


py_binary(
    name = "app",
    srcs = [
        "app.py",
        "__main__.py"
    ],
    main = "__main__.py",
    deps = [
        "@pip//cowsay",
        # Add torch to feel a giant dep. Actually not used.
        "@pip//torch",
    ],
)
