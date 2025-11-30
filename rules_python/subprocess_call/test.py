"""A simple site-packages test."""
 
import sys
import subprocess

subprocess.run([sys.executable, "-m", "datamodel_code_generator", "--version"], check=True)
