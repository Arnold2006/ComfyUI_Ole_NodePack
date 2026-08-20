# IdeoWildcard

ComfyUI CLIP encoder node that resolves `__token__` wildcard values inside an Ideogram4 JSON prompt and encodes the result into CONDITIONING for direct use with samplers.

## Installation

Clone this repository into your ComfyUI custom nodes directory:

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/Arnold2006/IdeoWildcard.git
```

This will install the node at:

```text
ComfyUI/custom_nodes/IdeoWildcard
```

Restart ComfyUI after cloning.

## Nodes

### Ideogram Wildcard CLIP Encode (primary)

- **Class:** `IdeogramWildcardCLIPEncode`
- **Display name:** `Ideogram Wildcard CLIP Encode`
- **Category:** `Ideogram`

Resolves wildcard tokens in a JSON prompt and encodes the resolved text with a CLIP model, producing CONDITIONING output that can be wired directly into a sampler.

#### Inputs

- `clip` (`CLIP`): the CLIP model used for text encoding
- `prompt` (`STRING`, multiline): raw JSON prompt text containing wildcard tokens

#### Outputs

- `conditioning` (`CONDITIONING`): encoded conditioning ready for a sampler
- `decoded_prompt` (`STRING`): the resolved JSON prompt text (useful for debugging)

> **Note:** This node re-executes on every queue run to produce a fresh random wildcard selection (no seed control).

---

### Ideogram Wildcard Prompt (legacy)

- **Class:** `IdeogramWildcardNode`
- **Display name:** `Ideogram Wildcard Prompt`
- **Category:** `Ideogram`

Resolves wildcard tokens and outputs the resolved JSON string without CLIP encoding.

#### Inputs

- `prompt` (`STRING`, multiline): raw JSON prompt text
- `seed` (`INT`): seed used for reproducible random line selection

#### Output

- `STRING`: the JSON prompt with any wildcard tokens resolved

## Wildcard syntax

Any string value that matches the exact pattern `__token__` will be treated as a wildcard.

For example:

```json
{
  "aesthetics": "__aesthetics__",
  "lighting": "__lighting__",
  "photo": "__photo__",
  "background": "__background__"
}
```

When the node runs, it looks for:

- `wildcards/aesthetics.txt`
- `wildcards/lighting.txt`
- `wildcards/photo.txt`
- `wildcards/background.txt`

The node ignores blank lines and comment lines beginning with `#`, then selects one random remaining line from each file using the provided seed.

If a wildcard file does not exist, the token is left unchanged and a warning is printed.

## Adding custom wildcards

1. Create a new text file inside the `wildcards/` folder.
2. Name the file to match the token, such as `mood.txt`.
3. Add one option per line.
4. Reference it in your JSON as `__mood__`.

Example file:

```text
# wildcards/mood.txt
playful and bright
dark and mysterious
elegant and minimal
```

## Example usage

Input JSON:

```json
{
  "subject": "fashion portrait of a model",
  "aesthetics": "__aesthetics__",
  "lighting": "__lighting__",
  "photo": "__photo__",
  "background": "__background__",
  "prompt": "clean composition, premium color grading"
}
```

Possible output:

```json
{
  "subject": "fashion portrait of a model",
  "aesthetics": "editorial fashion",
  "lighting": "soft diffused studio light",
  "photo": "medium format portrait",
  "background": "minimalist white studio",
  "prompt": "clean composition, premium color grading"
}
```