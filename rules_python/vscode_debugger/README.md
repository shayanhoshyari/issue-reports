# rules_python + Vcode debugger

- You need a venv (no dep in venv needed). You can get one with `./bazel run //requirements:venv`.
- Open vscode, and ensure `python`, and `bazel` extensions are installed.
- `Bazel: run py run`
- Select `//:app`
- See breakpoints working in both main process (`mattress`) and subprocess (`mattress/command.py`).

## Repro rules_python bug

To see the bug, move `sitecustomize.py` and its portion of `BUILD` to separate `debugpy` folder.

- Then if you run:
    ```
    $ ./bazel run --@rules_python//python/config_settings:debugger=//debugpy //:app
    ```
    it prints `[]` for the `sys.path` that contains `debugpy`.
- But if you add `//debugpy` explcitly to deps of `//:app`, you correctly see the import.
