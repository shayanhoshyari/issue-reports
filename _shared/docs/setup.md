# Environment Setup


## Direnv

This repository relies on **direnv** to manage development environments and path configurations (e.g., exposing the shared `bazel` proxy).

### 1. Install direnv

- **macOS**: `brew install direnv`
- **Linux**: Refer to the [official installation guide](https://direnv.net/docs/installation.html).

### 2. Hook into Shell

Add the hook to your shell configuration (e.g., `~/.zshrc`, `~/.bashrc`):

```bash
eval "$(direnv hook <your_shell_name>)"
```

### 3. Activate

Run the following in the repository root:

```bash
direnv allow
```
