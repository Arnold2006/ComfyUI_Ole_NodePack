import json
import random
import re
from pathlib import Path

try:
    import torch  # noqa: F401 – available inside ComfyUI runtime
except ImportError:  # allow loading outside ComfyUI (tests, linting)
    torch = None

TOKEN_PATTERN = re.compile(r"__([A-Za-z0-9._-]+)__")


class IdeogramWildcardNode:
    WILDCARDS_DIR = Path(__file__).resolve().parent / "wildcards"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"multiline": True, "default": "{}"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xFFFFFFFFFFFFFFFF}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "resolve"
    CATEGORY = "Ole NodePack"

    def resolve(self, prompt, seed):
        rng = random.Random(seed)
        cache = {}

        try:
            prompt_data = json.loads(prompt)
        except json.JSONDecodeError:
            # Plain text prompt: resolve wildcard tokens directly
            resolved = self._resolve_token(prompt, rng, cache)
            return (resolved,)

        resolved_prompt = self._resolve_value(prompt_data, rng, cache)
        return (json.dumps(resolved_prompt, indent=2, ensure_ascii=False),)

    def _resolve_value(self, value, rng, cache):
        if isinstance(value, dict):
            return {key: self._resolve_value(item, rng, cache) for key, item in value.items()}
        if isinstance(value, list):
            return [self._resolve_value(item, rng, cache) for item in value]
        if isinstance(value, str):
            return self._resolve_token(value, rng, cache)
        return value

    def _resolve_token(self, value, rng, cache):
        def _replace(match):
            token_name = match.group(1)
            if token_name not in cache:
                cache[token_name] = self._load_wildcard_options(token_name)

            options = cache[token_name]
            if not options:
                print(
                    f"[IdeogramWildcardNode] Warning: no wildcard entries available for '{token_name}'."
                )
                return match.group(0)

            return rng.choice(options)

        return TOKEN_PATTERN.sub(_replace, value)

    def _load_wildcard_options(self, token_name):
        wildcard_path = self.WILDCARDS_DIR / f"{token_name}.txt"
        if not wildcard_path.is_file():
            print(
                f"[IdeogramWildcardNode] Warning: wildcard file not found for '{token_name}': "
                f"{wildcard_path}"
            )
            return []

        return [
            line.strip()
            for line in wildcard_path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]


class IdeogramWildcardCLIPEncode:
    """Resolves Ideogram wildcard tokens and encodes the result with a CLIP
    model, outputting CONDITIONING that can be wired directly into a sampler.
    """

    WILDCARDS_DIR = Path(__file__).resolve().parent / "wildcards"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "clip": ("CLIP",),
                "prompt": ("STRING", {"multiline": True, "default": "{}"}),
            }
        }

    RETURN_TYPES = ("CONDITIONING", "STRING")
    RETURN_NAMES = ("conditioning", "decoded_prompt")
    FUNCTION = "encode"
    CATEGORY = "Ole NodePack"
    OUTPUT_NODE = False

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        # Return NaN so ComfyUI always re-executes (NaN != NaN),
        # ensuring a fresh random wildcard pick every run.
        return float("NaN")

    def encode(self, clip, prompt):
        # Resolve wildcards using random choices (no seed control)
        rng = random.Random()
        cache = {}
        resolver = IdeogramWildcardNode()
        resolver.WILDCARDS_DIR = self.WILDCARDS_DIR

        try:
            prompt_data = json.loads(prompt)
        except json.JSONDecodeError:
            # Plain text prompt: resolve wildcard tokens directly
            resolved_text = resolver._resolve_token(prompt, rng, cache)
        else:
            resolved_prompt = resolver._resolve_value(prompt_data, rng, cache)
            resolved_text = json.dumps(resolved_prompt, indent=2, ensure_ascii=False)

        # Encode with the CLIP model
        tokens = clip.tokenize(resolved_text)
        output = clip.encode_from_tokens(tokens, return_pooled=True, return_dict=True)
        cond = output.pop("cond")
        conditioning = [[cond, output]]

        return (conditioning, resolved_text)
