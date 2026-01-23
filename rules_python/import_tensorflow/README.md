# Bazel Template

This directory contains a template for creating new isolated Bazel workspaces in this repository.

## Setup

1.  Copy this folder to your new location:
    ```bash
    cp -r _shared/bazel-template/ rules_python/my_new_case/
    ```
2.  Customize `MODULE.bazel` (name, dependencies).
3.  Customize `BUILD` and sources.

## VS Code Integration

This template is configured for VS Code with the Python extension.

-   **Python Interpreter**: The `.vscode/settings.json` is configured to use a wrapper script at `.vscode/python`.
    -   This script invokes `bazel run @rules_python//python/bin:python`, which runs the Python interpreter managed by Bazel (`rules_python`).
    -   This ensures you don't need a system Python installed and that your editor uses the exact same Python version as your build.
-   **Debugging**: `launch.json` is configured to run tests and binaries using `debugpy` through Bazel.

## Directory Structure

-   `.vscode/`: Editor configuration.
-   `requirements/`: Python dependencies (using `rules_uv`).
-   `MODULE.bazel`: Bzlmod definition.
-   `REPO.bazel`: Repository boundary and configuration.
