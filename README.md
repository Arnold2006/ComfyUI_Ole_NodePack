# ComfyUI_Ole_NodePack

A single ComfyUI custom node pack combining three previously separate
projects into one installable repository. Every node in this pack lives
under its own **"Ole NodePack"** category in the ComfyUI node search/menu.

## Included nodes

### Ideogram 4 Prompt Builder

A self-contained node with a visual bbox editor: draw regions on a blank
canvas, set each region's type/desc/text/color palette, and assemble the
Ideogram 4 JSON caption prompt. Originally
[Ideogram-4-prompt-builder](https://github.com/Arnold2006/Ideogram-4-prompt-builder).

- **Class:** `Ideogram4PromptBuilderOLE`
- **Display name:** `Ideogram 4 Prompt Builder`

See the [canvas editor controls](#ideogram-4-editor) below for usage details.

### Resolution Sync

A frontend-only extension that live-syncs the **Resolution Selector** node's
calculated width/height into the **Ideogram 4 Prompt Builder** canvas —
*before* you queue the workflow. Originally
[ComfyUI-Resolution-Sync](https://github.com/Arnold2006/ComfyUI-Resolution-Sync).

It listens for changes on the Resolution Selector's `aspect_ratio` /
`megapixels` widgets, recalculates width/height in JavaScript (mirroring
ComfyUI's own Python math), and pushes the result straight into the Prompt
Builder's widgets — including triggering its internal redraw.

### Ideogram Wildcard

Nodes that resolve `__token__` wildcard values inside an Ideogram 4 JSON
prompt, optionally encoding the result directly with a CLIP model. Originally
[IdeoWildcard](https://github.com/Arnold2006/IdeoWildcard).

- **Class:** `IdeogramWildcardCLIPEncode` — **Display name:** `Ideogram Wildcard CLIP Encode`
  Resolves wildcard tokens in a JSON prompt and encodes the resolved text with
  a CLIP model, producing `CONDITIONING` output that can be wired directly
  into a sampler. Re-executes on every queue run for a fresh random pick.
- **Class:** `IdeogramWildcardNode` — **Display name:** `Ideogram Wildcard Prompt`
  Resolves wildcard tokens and outputs the resolved JSON string (seeded, for
  reproducible selection) without CLIP encoding.

Any string value that matches the exact pattern `__token__` is resolved
against a matching `wildcards/<token>.txt` file (blank lines and `#` comments
are ignored). Add your own wildcards by creating a new file inside
`ole_nodepack/wildcards/` named after the token, with one option per line.

## Installation

1. Clone this repository into your ComfyUI `custom_nodes` folder:

   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/Arnold2006/ComfyUI_Ole_NodePack.git
   ```

2. Install the pack's Python dependencies (from the ComfyUI Python
   environment):

   ```bash
   cd ComfyUI_Ole_NodePack
   pip install -r requirements.txt

   G:\ComfyUI\python_embeded\python.exe -m pip install -r G:\ComfyUI\ComfyUI\custom_nodes\ComfyUI_Ole_NodePack\requirements.txt
   ```

3. Restart ComfyUI. All nodes register themselves automatically on startup.

## Usage

In the ComfyUI node search, look under the **"Ole NodePack"** category (or
search by node name) to find the **Ideogram 4 Prompt Builder** and **Ideogram
Wildcard** nodes. Set the `background`, style, and region/bbox fields on the
prompt builder, then wire the `prompt` output into an Ideogram Wildcard node
(or directly to whatever sends the caption JSON to Ideogram 4). Add a
**Resolution Selector** node (`Add Node → utils → Resolution Selector`) if
you want its `aspect_ratio` / `megapixels` widgets to live-drive the prompt
builder's canvas size.

### Ideogram 4 editor

The prompt builder ships with a visual canvas editor (docked on the node) for
drawing and managing regions directly on the canvas instead of hand-editing
JSON:

- Drag: draw a new region · Ctrl/Cmd-drag: force-draw even on top of another
- Click: select a region · Alt-click: cycle overlapping regions
- Double-click: edit the description inline
- Right-click: region list (select / delete / duplicate / reorder, top = front)
- Del / Backspace: remove the selected region
- Ctrl/Cmd + C / V / D: copy / paste / duplicate the selected region
- Color swatches: click to edit, drag to reorder, right-click to remove
- Toolbar: Live sampling preview as background, Grab BG / Clear BG, brightness
  slider, token estimate, and Copy / Paste / Clear all, plus named JSON
  templates saved on the ComfyUI server

The editor's front-end (`web/js/ideogram4_prompt_builder.js` and
`web/js/utility.js`) is adapted from the equivalent node/editor in
[kijai/ComfyUI-KJNodes](https://github.com/kijai/ComfyUI-KJNodes) (GPL-3.0),
renamed to match this node's identifiers; see `LICENSE`.

## Repository layout

```text
__init__.py                        # combined ComfyUI entry point
ole_nodepack/
  ideogram_4_prompt_builder.py      # Ideogram 4 Prompt Builder node
  ideogram_wildcard_node.py         # Ideogram Wildcard nodes
  fonts/FreeMono.ttf                # font used by the prompt builder's preview render
  wildcards/*.txt                   # default wildcard token files
web/
  js/ideogram4_prompt_builder.js    # prompt builder canvas editor front-end
  js/utility.js                     # shared front-end helpers
  resolution_sync.js                # Resolution Selector <-> prompt builder sync
tests/
  test_ideogram_wildcard_node.py    # unit tests for the wildcard nodes
```
