# Missing files when running with `venvs_site_packages=yes`

Description: https://github.com/bazel-contrib/rules_python/issues/3470#issuecomment-3679757819

Quick repro steps
```
# On linux run 
./bazel build //:app
```


Observe that

- `bazel-bin/app.runfiles/_main/_app.venv/lib/python3.13/site-packages/nvidia/nccl//lib/libnccl.so.2` must exist, but is missing.
- As a side note, `bazel-bin/app.runfiles/rules_python++pip+pip_313_nvidia_nccl_cu12_py3_none_manylinux_2_17_x86_64_ad730cf1/site-packages/nvidia/nccl/lib/libnccl.so.2` exists, so the wheel does define the runfile.
