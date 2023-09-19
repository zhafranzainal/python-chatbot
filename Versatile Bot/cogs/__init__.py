from os.path import dirname, basename, isfile, join

import glob

# Find all Python files in the current directory
modules_path = glob.glob(join(dirname(__file__), "*.py"))

# List all module names
__all__ = [
    basename(f)[:-3]  # For each file, extract module name (excluding '.py' extension)
    for f in modules_path  # Iterate over file paths found by glob.glob
    if isfile(f) and not f.endswith('__init__.py')  # Check if file instead of folder, and not initialization file
]
