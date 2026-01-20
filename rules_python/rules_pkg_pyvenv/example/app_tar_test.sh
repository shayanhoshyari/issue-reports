#!/bin/bash
set -e

# Create a temporary directory for extraction
EXTRACT_DIR=$(mktemp -d)
trap 'rm -rf "$EXTRACT_DIR"' EXIT

echo "Extracting tarballs to $EXTRACT_DIR..."

# APP_TAR_FILES contains a space-separated list of paths to the tar files
# We can iterate over them directly.
# The paths are relative to the runfiles root, which is what we want.
for tar_file in $APP_TAR_FILES; do
  echo "Extracting $tar_file..."
  tar -xf "$tar_file" -C "$EXTRACT_DIR"
done

echo "Running entrypoint..."
# The entrypoint script is at the root of the extraction
if [ ! -f "$EXTRACT_DIR/entrypoint" ]; then
  echo "Error: entrypoint script not found in extracted files"
  exit 1
fi

# Execute the entrypoint
"$EXTRACT_DIR/entrypoint"

echo "Test passed!"
