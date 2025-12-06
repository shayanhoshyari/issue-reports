# Symlinks in .venv not having `File.is_symlink = True`

Related to: ...

## How to repro:

```
bazel run //:runfiles
```

to get the runfiles.txt for the //:test target which is just a py_binary that uses torch.

If you open the created file `bazel-bin/runfiles.txt`, you will see:


For folders that we don't have file conflicts or .so files, we indeed see:
```
- bazel-out/darwin_arm64-fastbuild/bin/_test.venv/lib/python3.13/site-packages/filelock
- _test.venv/lib/python3.13/site-packages/filelock
- True

- bazel-out/darwin_arm64-fastbuild/bin/_test.venv/lib/python3.13/site-packages/fsspec
- _test.venv/lib/python3.13/site-packages/fsspec
- True

...
```

The file under .venv indeed has is_symlink = True

However, for folders that need to resolve to individual files (e.g. torch), we see:

```
- bazel-out/darwin_arm64-fastbuild/bin/_test.venv/lib/python3.13/site-packages/torch/_C.cpython-313-darwin.so
- _test.venv/lib/python3.13/site-packages/torch/_C.cpython-313-darwin.so
- False

...
```

The individual resolved files have `is_symlink = False`!

If we actually look at the runfile after building the target, we also see its target is an abs path:

```
./bazel build :test

ls -al bazel-bin/test.runfiles/_main/_test.venv/lib/python3.13/site-packages/torch/_C.cpython-313-darwin.so 

lrwxr-xr-x  1 hoshyari  wheel  188 Dec  5 22:19 bazel-bin/test.runfiles/_main/_test.venv/lib/python3.13/site-packages/torch/_C.cpython-313-darwin.so -> /private/var/tmp/_bazel_hoshyari/0915edf9aa0fc6e009ba2664be204381/execroot/_main/bazel-out/darwin_arm64-fastbuild/bin/_test.venv/lib/python3.13/site-packages/torch/_C.cpython-313-darwin.so
```

## What is the issue

For building docker images, it is very common to make .tar files.

Currently, `tar.bzl` (used for aspect_rules_py, rules_oci, ... family) does not support symlinks, but there an ongoing thread about it: <https://github.com/bazel-contrib/tar.bzl/issues/16>

A suggestion by @rickeylev is to use the `File.is_symlink` field to determine if a file is a symlink and just write as-is as symlink and preserve the relative path.

I did implement a basic tar rule equivalent based on this idea at: <https://github.com/bazel-contrib/rules_python/issues/3388#issuecomment-3615363362>

However, with current result, the torch `.so` files return `File.is_symlink = False`, so we will end up writing the file to the tar twice (once the external runfile and once the one under .venv), and it can double the size of the tar (image layer). 


## Experimental change

Uncommetning 

```
# git_override(
#     module_name = "rules_python",
#     remote = "https://github.com/shayanhoshyari/rules_python.git",
#     commit = "f48fdc08cec73e7440fc436935b8142054128bbc",
# )
```

to use <https://github.com/bazel-contrib/rules_python/pull/3440> in `MODULE.bazel`, I do get the same runfiles tree, but with `File.is_symlink = True` for the torch `.so` files.