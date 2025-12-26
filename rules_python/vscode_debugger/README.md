# rules_python + Vcode debugger

- You need a venv (no dep in venv needed). You can get one with `./bazel run //requirements:venv`.
- Open vscode, and ensure `python`, and `bazel` extensions are installed.
- `Bazel: run py run`
- Select `//:app`
- See breakpoints working in both main process (`mattress`) and subprocess (`mattress/command.py`).

## Repro rules_python bug

I have made a hook to add a `.pth` file or `sitecustomize.py` file to the `sys.path` so the executable can connect to the debugger.

For easy debugging, at beginning of runtime, I print if the hook is on the path.

It is expected that all these 6 variants work, but 2 and 3 don't work. 4, 5, 6 are not really practical and are just here to show that
the py_library for the hook is defined correctly 

| # | Summary | Command | Works |
|---|---------|---------|-------|
| 1 | --debugger + put in root | `./bazel run //:app --@rules_python//python/config_settings:debugger=//:debugpy` | ✅ |
| 2  | --debugger +  put in venv site-packages | `./bazel run //:app --@rules_python//python/config_settings:debugger=//debugpy:venv` | ❌ |
| 3 | --debugger +  use imports | `./bazel run //:app --@rules_python//python/config_settings:debugger=//debugpy:imports` | ❌ |
| 4 | explicit dep + put in root | Add `//:debugpy` to `//:app.deps` + `./bazel run //:app` | ✅ |
| 5 | explicit dep + put in venv site-packages | Add `//debugpy:venv` to `//:app.deps` + `./bazel run //:app` | ✅ |
| 6 | explicit dep + use imports | Add `//debugpy:imports` to `//:app.deps` + `./bazel run //:app` | ✅ |

