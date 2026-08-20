# ComfyUI Resolution Sync

A tiny ComfyUI frontend extension that live-syncs the **Resolution Selector** node's calculated width/height into an **Ideogram 4 Prompt Builder** canvas — *before* you queue the workflow.

It supports both [Arnold2006's Ideogram 4 Prompt Builder](https://github.com/Arnold2006/Ideogram-4-prompt-builder) (`Ideogram4PromptBuilderOLE`) and [KJNodes' Ideogram 4 Prompt Builder](https://github.com/kijai/ComfyUI-KJNodes) (`Ideogram4PromptBuilderKJ`).

## Why

The Ideogram 4 Prompt Builder nodes use their `width`/`height` widgets to set the aspect ratio of their interactive drawing canvas. Normally, connecting `ResolutionSelector`'s outputs to them only updates the value at execution time (when you hit Queue Prompt) — which is too late if you're drawing bounding boxes on the canvas *before* running the workflow.

This extension listens for changes on the Resolution Selector's `aspect_ratio` / `megapixels` widgets, recalculates width/height in JavaScript (mirroring ComfyUI's own Python math), and pushes the result straight into the Prompt Builder's widgets — including triggering its internal redraw — the moment you change the dropdown. The rounding step and min/max are matched to each target node's own requirements (multiples of 16 for `Ideogram4PromptBuilderOLE`, multiples of 8 for `Ideogram4PromptBuilderKJ`).

## Requirements

- ComfyUI (core `ResolutionSelector` node from `comfy_extras`)
- One of:
  - [Ideogram-4-prompt-builder](https://github.com/Arnold2006/Ideogram-4-prompt-builder) installed, for the `Ideogram4PromptBuilderOLE` node
  - [ComfyUI-KJNodes](https://github.com/kijai/ComfyUI-KJNodes) installed, for the `Ideogram4PromptBuilderKJ` node

## Installation

1. Clone this repo into your `custom_nodes` folder:
   ```bash
   cd ComfyUI/custom_nodes
   git clone https://github.com/YOUR_USERNAME/comfyui-resolution-sync.git
   ```
2. Restart ComfyUI.
3. Confirm it loaded — you should see `resolution_sync` listed among the loaded custom node modules in the ComfyUI server console on startup.

## Usage

1. Add a **Resolution Selector** node (`Add Node → utils → Resolution Selector`).
2. Add an **Ideogram 4 Prompt Builder** node (either `Ideogram4PromptBuilderOLE` or KJNodes' `Ideogram4PromptBuilderKJ`).
3. **Do not** connect Resolution Selector's `width`/`height` outputs to the Prompt Builder's inputs — leave the Prompt Builder's `width`/`height` as plain widgets (not converted to inputs).
4. Change the Resolution Selector's `aspect_ratio` or `megapixels` value. The Ideogram 4 Prompt Builder's canvas should immediately resize to match, before you ever queue the workflow.

## How it works

`web/resolution_sync.js` registers a ComfyUI frontend extension that:

1. Hooks into the `callback` of the `aspect_ratio` and `megapixels` widgets on any `ResolutionSelector` node.
2. On change, recalculates width/height locally (matching the Python `execute()` logic: aspect ratio × target megapixels, rounded to the target node's required step — 16 for `Ideogram4PromptBuilderOLE`, 8 for `Ideogram4PromptBuilderKJ` — and clamped to its min/max).
3. Finds whichever supported Prompt Builder node type is present on the canvas (checking `Ideogram4PromptBuilderOLE` first, then `Ideogram4PromptBuilderKJ`) and sets its `width`/`height` widget values.
4. **Crucially**, also invokes those widgets' own `callback` functions (not just setting `.value`) — this is what actually triggers the Prompt Builder's internal canvas to redraw. Setting `.value` alone updates the number but doesn't trigger the node's visual update, since ComfyUI custom canvas nodes typically hook their redraw logic into the widget callback rather than watching the value directly.

## Limitations / notes

- This targets the *first* matching node of each type found on the canvas (`app.graph._nodes.find(...)`). If you have multiple Resolution Selector nodes, or multiple Prompt Builder nodes of the same type, in one workflow, only the first of each will sync. If both `Ideogram4PromptBuilderOLE` and `Ideogram4PromptBuilderKJ` are present, both will be synced.
- The width/height rounding logic is inferred from ComfyUI's `ResolutionSelector` node behavior — if a future ComfyUI update changes that node's math, this script's local calculation may drift slightly out of sync with the "official" execution-time value. Worth spot-checking after ComfyUI core updates.
- This is a UI-only sync; it doesn't change what data flows through the graph at execution time. The Ideogram node's `width`/`height` widgets are set independently — they are not wired to the Resolution Selector via a graph link.

## License

MIT
