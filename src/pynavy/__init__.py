import os, sys

# dont know why __init__.py cannot import modules when package is imported
# this workaround works by including module folder to path
module_folder = os.path.dirname(os.path.abspath(__file__))
sys.path.append(module_folder)
