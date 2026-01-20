# Repository Conventions

## Directory Structure
The repository is organized by technology category and specific case:

`<category> / <case name or subject> / ...code...`

### Categories
- **`rules_python/`**: Python-related Bazel issues, debugging, and environments.
- **`bazelbuild/`**: Core Bazel functionality and "Make" variable experiments.
- **`rules_img/`**: Container image rules.
- **`_shared/`**: Common infrastructure (scripts, docs).

## Usage Guidelines
1.  **Isolation**: Each subdirectory is a standalone project. Do not try to build from the root.
2.  **Navigation**: `cd` into a specific case folder to run commands.
3.  **Tooling**: Tools needed to be installed a-priori, e.g. `bazel`, are provided via `_shared/bin` and added to your `PATH` automatically by `direnv`.

## Bazel Workspace Setup

Each isolated case should be a valid Bazel workspace.

### Required Files

Every workspace must contain:

-   `MODULE.bazel`: Dependencies and module definition.
-   `BUILD`: Root build file.
-   `.bazelrc`: Configuration flags.
-   `.bazelversion`: Specifies the Bazel version (use latest stable, e.g., 7.4.1).
-   `.vscode/`: VS Code configuration (settings, launch configurations).

### Template

A standard template is available at `_shared/bazel-template/`.
You can copy this template to start a new case:

```bash
cp -r _shared/bazel-template/ new_case_folder/
```

### Python Projects

For Python projects, we recommend using `rules_uv` for dependency management.

-   Define dependencies in `requirements/requirements.in`.
-   Use `rules_uv`'s `pip_compile` to generate `requirements.txt` (or lock file).
