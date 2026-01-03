# Examples demonstrating "Make" variables

These examples demonstrate Bazel's ["Make" variable](https://bazel.build/reference/be/make-variables)
support.

## Predefined variables
`//testapp:show_predefined_variables` demonstrates predefined variables
available to all rules. These are parsed in any attribute marked "Subject to
'Make Variable' substitution".
```
$ bazel build //testapp:show_predefined_variables && cat bazel-bin/testapp/show_predefined_variables.out
COMPILATION_MODE: fastbuild
BINDIR: bazel-out/x86-fastbuild/bin
GENDIR: bazel-out/x86-fastbuild/bin
TARGET_CPU: x86
```

## Predefined genrule variables

### All genrules
`//testapp:show_genrule_variables` demonstrates predefined variables exclusively
available to `genrule`.
```
$ bazel build //testapp:show_genrule_variables && cat bazel-bin/testapp/subdir/show_genrule_variables1.out
SRCS: testapp/show_genrule_variables1.src testapp/show_genrule_variables2.src
OUTS: bazel-out/x86-fastbuild/bin/testapp/subdir/show_genrule_variables1.out bazel-out/x86-fastbuild/bin/testapp/subdir/show_genrule_variables2.out
RULEDIR: bazel-out/x86-fastbuild/bin/testapp
@D (prefer RULEDIR to this): bazel-out/x86-fastbuild/bin/testapp
 * Because this genrule has multiple outputs, @D is the same as RULEDIR.
```

### Genrules with one input or output
`//testapp:single_file_genrule` demonstrates predefined variables exclusively
available to `genrule`s that consume a single source file or produce a single
output file.
```
$ bazel build //testapp:single_file_genrule && cat bazel-bin/testapp/subdir/single_file_genrule.out
<: testapp/show_genrule_variables1.src
@: bazel-out/x86-fastbuild/bin/testapp/subdir/single_file_genrule.out
RULEDIR: bazel-out/x86-fastbuild/bin/testapp
@D: bazel-out/x86-fastbuild/bin/testapp/subdir
 * Because this genrule has one input, < is a valid variable.
 * Because this genrule has one output, @ is a valid variable.
 * Because this genrule has one output, @D is different than RULEDIR.
```

## Predefined path variables

Docs: https://bazel.build/reference/be/make-variables#predefined_label_variables

`//testapp:show_app_output` demonstrates predefined variables related to source
and output paths.
```
$ bazelisk build //testapp:show_app_output && cat bazel-bin/testapp/app_output

:app output paths
 execpath: bazel-out/darwin_arm64-opt-exec/bin/testapp/app
 runfiles: testapp/app
 location: bazel-out/darwin_arm64-opt-exec/bin/testapp/app
 rlocationpath: _main/testapp/app

:app_target output paths
 execpath: bazel-out/darwin_arm64-fastbuild/bin/testapp/app_target
 runfiles: testapp/app_target
 location: bazel-out/darwin_arm64-fastbuild/bin/testapp/app_target
 rlocationpath: _main/testapp/app_target

source file paths
 execpath: testapp/empty.source
 runfiles: testapp/empty.source
 location: testapp/empty.source
 rlocationpath: _main/testapp/empty.source


another repo
 execpath: bazel-out/darwin_arm64-opt-exec/bin/external/rules_multitool++multitool+multitool/tools/gh/gh
 runfiles: ../rules_multitool++multitool+multitool/tools/gh/gh
 location: bazel-out/darwin_arm64-opt-exec/bin/external/rules_multitool++multitool+multitool/tools/gh/gh
 rlocationpath: rules_multitool++multitool+multitool/tools/gh/gh
```

Some historical notes

- First there was just `location`, but it turned out problematic as there was no way to distinguish when runfile path is needed vs. when path under workspace: https://github.com/bazelbuild/bazel/issues/2475#issuecomment-339318016, so `execpath`, `rootpath` were added. The names are not really helpful to tell one which is which.
- Then when bazel mod came out, the existence of external repos broke things + workspace, and they had to add `rlocationpath`: https://github.com/bazelbuild/bazel/issues/15029. Though onces workspaces go away I think we have  `rlocation path = os.path.join(_main, rootpath)`


## BUILD_WORKSPACE_DIRECTORY

```
$ bazelisk run //testapp:echo

BUILD_WORKSPACE_DIRECTORY=/Users/hoshyari/code/issue-reports/bazelbuild/make-variables
```

## Custom Starlark-defined variables
`//testapp:show_custom_var` demonstrates custom variable defined in Starlrak.
```
$ bazel build //testapp:show_custom_var && cat bazel-bin/testapp/custom_var
Target //testapp:show_custom_var up-to-date:
  bazel-bin/testapp/custom_var
INFO: Build completed successfully, 2 total actions
FOO is equal to bar!
```

