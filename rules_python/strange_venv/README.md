# Broken venv when dependency module is used


## Summary of the situation

```sh
# Participants
root_module = bazel module
rules_dummy = bazel module
rules_dummy//tool = py_binary
pip_rules_dummy = pip hub defined in rules_dummy

# Dependency structure
root_module.deps = [rules_dummy]
   @rules_dummy//tool.deps = [@pip_rules_dummy//cowsay, @pip_rules_dummy//google_cloud_storage]
        google_cloud_storage has a namespace package. 
        
# What does rules_dummy//tool do
1. Imports cowsay
2. Imports google.cloud.storage
```


## Issue

| Alias | Command | Issuer module | Imports cowsay | Imports google.cloud.storage |
| --- |---------|---------------|----------------|-----------------------------|
| `make run` | `bazelisk run @rules_dummy//tool` | root_module | ✅ | ❌ (bug) |
| `make run_rules_dummy` | `bazelisk run @rules_dummy//tool` | rules_dummy | ✅ | ✅ |

- Note this is a made up example for simplicity. In my real use-case, `@rules_dummy//tool` was a tool used in rules exported from `rules_dummy`. And those rules basically became unusable.
- The **wheels that have namespace packages** trigger this issue.
- This issue only happens `venvs_site_packages=yes`.
