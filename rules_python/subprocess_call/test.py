"""A simple site-packages test."""
 
import sys
import subprocess

print("sys.executable is", sys.executable)
subprocess.run([sys.executable, "-m", "datamodel_code_generator", "--version"], check=True)
