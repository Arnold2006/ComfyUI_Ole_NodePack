from .ideogram_wildcard_node import IdeogramWildcardCLIPEncode, IdeogramWildcardNode

NODE_CLASS_MAPPINGS = {
    "IdeogramWildcardNode": IdeogramWildcardNode,
    "IdeogramWildcardCLIPEncode": IdeogramWildcardCLIPEncode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "IdeogramWildcardNode": "Ideogram Wildcard Prompt",
    "IdeogramWildcardCLIPEncode": "Ideogram Wildcard CLIP Encode",
}

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS"]
