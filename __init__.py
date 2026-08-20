"""ComfyUI custom node package entry point for the Ole NodePack.

This pack combines three previously separate node packs into one:

- **Ideogram 4 Prompt Builder** — a visual bbox editor node that assembles the
  structured JSON caption prompt used by Ideogram 4.
- **Resolution Sync** — a frontend-only extension that live-syncs the
  Resolution Selector node's calculated width/height into the Ideogram 4
  Prompt Builder's canvas before the workflow is queued.
- **Ideogram Wildcard** — nodes that resolve `__token__` wildcard values
  inside an Ideogram 4 JSON prompt, optionally encoding the result directly
  with a CLIP model.

Cloning this repository into ComfyUI's `custom_nodes` folder and restarting
ComfyUI is enough for every node to be discovered. All nodes share a single
"Ole NodePack" category in the ComfyUI node search/menu.

Note: ComfyUI's custom node loader (see `load_custom_node` in `nodes.py`)
registers a package using *either* its legacy `NODE_CLASS_MAPPINGS` *or* its
`comfy_entrypoint`/`ComfyExtension` (V3 schema) hook, never both, from a
single `__init__.py`. Ideogram4PromptBuilderOLE is a V3 `io.ComfyNode`, but
`io.ComfyNode` subclasses remain fully compatible with the legacy mapping
(their `INPUT_TYPES`/`CATEGORY`/`RETURN_TYPES`/etc. are lazily derived from
`define_schema()`), so it is registered through `NODE_CLASS_MAPPINGS` here
alongside the Ideogram Wildcard nodes, keeping every node in this pack
discoverable together.
"""

from .ole_nodepack.ideogram_4_prompt_builder import Ideogram4PromptBuilderOLE
from .ole_nodepack.ideogram_wildcard_node import (
    IdeogramWildcardCLIPEncode,
    IdeogramWildcardNode,
)

# Front-end assets (the prompt builder's canvas editor and the resolution
# sync script) live in ./web and are picked up by ComfyUI independently of
# node registration, based on this module-level variable.
WEB_DIRECTORY = "./web"

NODE_CLASS_MAPPINGS = {
    "Ideogram4PromptBuilderOLE": Ideogram4PromptBuilderOLE,
    "IdeogramWildcardNode": IdeogramWildcardNode,
    "IdeogramWildcardCLIPEncode": IdeogramWildcardCLIPEncode,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "Ideogram4PromptBuilderOLE": "Ideogram 4 Prompt Builder",
    "IdeogramWildcardNode": "Ideogram Wildcard Prompt",
    "IdeogramWildcardCLIPEncode": "Ideogram Wildcard CLIP Encode",
}

__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
]
