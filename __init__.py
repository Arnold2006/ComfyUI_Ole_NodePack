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
"""

from comfy_api.latest import ComfyExtension, io

from .ole_nodepack.ideogram_4_prompt_builder import Ideogram4PromptBuilderOLE
from .ole_nodepack.ideogram_wildcard_node import (
    IdeogramWildcardCLIPEncode,
    IdeogramWildcardNode,
)

# Front-end assets (the prompt builder's canvas editor and the resolution
# sync script) live in ./web and are picked up by ComfyUI independently of
# comfy_entrypoint, based on this module-level variable.
WEB_DIRECTORY = "./web"

# Legacy-style registration, used by the Ideogram Wildcard nodes.
NODE_CLASS_MAPPINGS = {
    "IdeogramWildcardNode": IdeogramWildcardNode,
    "IdeogramWildcardCLIPEncode": IdeogramWildcardCLIPEncode,
}
NODE_DISPLAY_NAME_MAPPINGS = {
    "IdeogramWildcardNode": "Ideogram Wildcard Prompt",
    "IdeogramWildcardCLIPEncode": "Ideogram Wildcard CLIP Encode",
}


class OleNodePackExtension(ComfyExtension):
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [Ideogram4PromptBuilderOLE]


async def comfy_entrypoint() -> OleNodePackExtension:
    return OleNodePackExtension()


__all__ = [
    "NODE_CLASS_MAPPINGS",
    "NODE_DISPLAY_NAME_MAPPINGS",
    "WEB_DIRECTORY",
    "comfy_entrypoint",
]
