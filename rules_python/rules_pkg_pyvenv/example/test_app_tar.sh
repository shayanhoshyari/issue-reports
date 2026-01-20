#!/bin/bash
set -e

# These paths are relative to the test runfiles directory
# The tar files are provided as data dependencies
TAR_MAIN="example/app_tar.main.tar"
TAR_EXTERNAL="example/app_tar.external.tar"
TAR_TORCH="example/app_tar.torch.tar"
TAR_NVIDIA="example/app_tar.nvidia.tar"

# Create a temporary directory for extraction
EXTRACT_DIR=$(mktemp -d)
trap 'rm -rf "$EXTRACT_DIR"' EXIT

echo "Extracting tarballs to $EXTRACT_DIR..."

# Extract all tarballs
tar -xf "$TAR_MAIN" -C "$EXTRACT_DIR"
tar -xf "$TAR_EXTERNAL" -C "$EXTRACT_DIR"
# Check if these exist before extracting (they might be empty/non-existent depending on the build)
if [ -f "$TAR_TORCH" ]; then tar -xf "$TAR_TORCH" -C "$EXTRACT_DIR"; fi
if [ -f "$TAR_NVIDIA" ]; then tar -xf "$TAR_NVIDIA" -C "$EXTRACT_DIR"; fi

echo "Running entrypoint..."
# The entrypoint script is at the root of the extraction
if [ ! -f "$EXTRACT_DIR/entrypoint" ]; then
  echo "Error: entrypoint script not found in extracted files"
  exit 1
fi

# Execute the entrypoint
"$EXTRACT_DIR/entrypoint"

echo "Test passed!"
