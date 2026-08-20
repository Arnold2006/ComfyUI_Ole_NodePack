import sys
from pathlib import Path

# Allow tests to import modules from the ole_nodepack package directly
# (matching the upstream IdeoWildcard test's flat `from ideogram_wildcard_node
# import ...` style) without requiring the ComfyUI runtime to be installed.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "ole_nodepack"))
