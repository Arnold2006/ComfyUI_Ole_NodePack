"""ComfyUI custom node package entry point for the Ideogram 4 Prompt Builder.

Cloning this repository into ComfyUI's `custom_nodes` folder and restarting
ComfyUI is enough for the node to be discovered: ComfyUI imports this
`__init__.py`, calls `comfy_entrypoint()`, and registers every node class
returned by the extension's `get_node_list()`.
"""

from comfy_api.latest import ComfyExtension, io

from .ideogram_4_prompt_builder import Ideogram4PromptBuilderOLE

# Front-end assets (the node's canvas editor) live in ./web and are picked up by
# ComfyUI independently of comfy_entrypoint, based on this module-level variable.
WEB_DIRECTORY = "./web"


class Ideogram4PromptBuilderExtension(ComfyExtension):
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [Ideogram4PromptBuilderOLE]


async def comfy_entrypoint() -> Ideogram4PromptBuilderExtension:
    return Ideogram4PromptBuilderExtension()


__all__ = ["WEB_DIRECTORY", "comfy_entrypoint"]
