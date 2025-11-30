# Reproducer for [rules_python/issues/3437](https://github.com/bazel-contrib/rules_python/issues/3437) 

To reproduce the issue, run:

```
$ ./bazel run //:test

/private/var/tmp/_bazel_hoshyari/5bf493163e144814d5d8244a8cb0233d/execroot/_main/bazel-out/darwin_arm64-fastbuild/bin/test.runfiles/rules_python++python+python_3_13_aarch64-apple-darwin/bin/python3: No module named datamodel_code_generator
Traceback (most recent call last):
  File "/private/var/tmp/_bazel_hoshyari/5bf493163e144814d5d8244a8cb0233d/execroot/_main/bazel-out/darwin_arm64-fastbuild/bin/test.runfiles/_main/_test_stage2_bootstrap.py", line 499, in <module>
    main()
    ~~~~^^
  File "/private/var/tmp/_bazel_hoshyari/5bf493163e144814d5d8244a8cb0233d/execroot/_main/bazel-out/darwin_arm64-fastbuild/bin/test.runfiles/_main/_test_stage2_bootstrap.py", line 493, in main
    _run_py_path(main_filename, args=sys.argv[1:])
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/var/tmp/_bazel_hoshyari/5bf493163e144814d5d8244a8cb0233d/execroot/_main/bazel-out/darwin_arm64-fastbuild/bin/test.runfiles/_main/_test_stage2_bootstrap.py", line 287, in _run_py_path
    runpy.run_path(main_filename, run_name="__main__")
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen runpy>", line 287, in run_path
  File "<frozen runpy>", line 98, in _run_module_code
  File "<frozen runpy>", line 88, in _run_code
  File "/private/var/tmp/_bazel_hoshyari/5bf493163e144814d5d8244a8cb0233d/execroot/_main/bazel-out/darwin_arm64-fastbuild/bin/test.runfiles/_main/test.py", line 6, in <module>
    subprocess.run([sys.executable, "-m", "datamodel_code_generator", "--version"], check=True)
    ~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/var/tmp/_bazel_hoshyari/5bf493163e144814d5d8244a8cb0233d/external/rules_python++python+python_3_13_aarch64-apple-darwin/lib/python3.13/subprocess.py", line 577, in run
    raise CalledProcessError(retcode, process.args,
                             output=stdout, stderr=stderr)
subprocess.CalledProcessError: Command '['/private/var/tmp/_bazel_hoshyari/5bf493163e144814d5d8244a8cb0233d/execroot/_main/bazel-out/darwin_arm64-fastbuild/bin/test.runfiles/rules_python++python+python_3_13_aarch64-apple-darwin/bin/python3', '-m', 'datamodel_code_generator', '--version']' returned non-zero exit status 1.
```

To see that `rules_python < 1.7.0` don't have this issue, change `MODULE.bazel` to use `rules_python == 1.6.3` and retry:

```
$ ./bazel run //:test

0.36.0
```
