# rules_pkg_pyvenv

`rules_pkg_pyvenv` provides a `tar_runfiles` rule that packages the runfiles of a `py_binary` into multiple tarballs. This is particularly useful for building efficient OCI images where you want to separate frequently changing application code from stable dependencies.

## Purpose

The `tar_runfiles` rule addresses limitations in existing packaging rules by correctly handling symlinks and providing a way to split runfiles into logical "layers":
- `main`: Application code and symlinks (usually small, changes often).
- `external`: External dependencies (large, changes less often).
- Specialized layers for heavy packages like `torch` or `nvidia` to improve cacheability.

## Context & Motivation

This rule was created to address current limitations in Bazel's packaging ecosystem, specifically regarding the handling of `SymlinkEntry` in runfiles. For more context, see [rules_python issue #3523](https://github.com/bazel-contrib/rules_python/issues/3523#issuecomment-3771157032).

At the moment, standard packaging tools do not fully support the `SymlinkEntry` structure used by `rules_python` when the new feature [venv_site_packages](https://github.com/bazel-contrib/rules_python/issues) is enabled.`tar_runfiles` provides a workaround by manually iterating over runfiles and symlinks to build correct tarballs.

Once packaging tools (like `rules_pkg` or OCI rules) natively support `SymlinkEntry`, this rule will likely become redundant.

## Requirements

- **rules_python**: 1.8.0

> [!NOTE]
> This repository is intended as an example/reference implementation. As `rules_python` evolves, internal changes might be necessary to maintain compatibility.

## Usage

### Option 1: Copy to your project

You can copy the `private/` directory and `defs.bzl` into your workspace and load the rule locally.

```python
load("//:defs.bzl", "tar_runfiles")

py_binary(
    name = "app",
    srcs = ["main.py"],
)

tar_runfiles(
    name = "app_tar",
    py_binary = ":app",
)
```

### Option 2: git_override

In your `MODULE.bazel`, you can use `git_override` to point to this repository:

```python
bazel_dep(name = "rules_pkg_pyvenv", version = "0.0.0")
git_override(
    module_name = "rules_pkg_pyvenv",
    remote = "https://github.com/your-username/issue-reports.git",
    strip_prefix = "rules_python/rules_pkg_pyvenv",
    commit = "...",
)
```

## Example

An example usage can be found in the `example/` directory. You can run the tests to see it in action:

```bash
bazel test //example:app_tar_test
```