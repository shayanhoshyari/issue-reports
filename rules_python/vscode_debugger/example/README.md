# rules_python + Vcode debugger

- You need a python with `bazel_debugpy` installed. You can use the `rules_uv` venv, `./bazel run //requirements:venv`.
- `Bazel: run py run`
- Select `//:app`
- See breakpoints working in both main process (`mattress`) and subprocess (`mattress/command.py`).
