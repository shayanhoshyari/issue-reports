load("@rules_pkg_pyvenv//:defs.bzl", "tar_runfiles")
load("@rules_python//python:defs.bzl", "py_binary")
load("@rules_shell//shell:sh_test.bzl", "sh_test")

py_binary(
    name = "app",
    srcs = ["__main__.py"],
    main = "__main__.py",
    deps = [
        "@rules_pkg_pyvenv_pip_dev//cowsay",
        "@rules_pkg_pyvenv_pip_dev//google_cloud_storage",
    ],
)

# You can now use :app_tar as layers in rules_oci or rules_img
tar_runfiles(
    name = "app_tar",
    py_binary = ":app",
)

# A test to make the layers work. Test just extracts them and tries
# to run the entrypoint.
sh_test(
    name = "app_tar_test",
    srcs = ["app_tar_test.sh"],
    data = [":app_tar"],
    env = {
        "APP_TAR_FILES": "$(rootpaths :app_tar)",
    },
)


