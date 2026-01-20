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
