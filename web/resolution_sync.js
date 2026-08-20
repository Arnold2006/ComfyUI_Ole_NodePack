import { app } from "/scripts/app.js";

const ASPECT_RATIOS = {
  "1:1 (Square)": [1, 1],
  "3:2 (Photo)": [3, 2],
  "4:3 (Standard)": [4, 3],
  "16:9 (Widescreen)": [16, 9],
  "21:9 (Ultrawide)": [21, 9],
  "2:3 (Portrait Photo)": [2, 3],
  "3:4 (Portrait Standard)": [3, 4],
  "9:16 (Portrait Widescreen)": [9, 16],
};

// Target node types to sync into, in priority order, each with the rounding
// step and min/max their width/height widgets require.
const TARGET_NODE_TYPES = [
  // Arnold2006/Ideogram-4-prompt-builder — requires multiples of 16.
  { comfyClass: "Ideogram4PromptBuilderOLE", step: 16, min: 64, max: 16384 },
  // kijai/ComfyUI-KJNodes — requires multiples of 8.
  { comfyClass: "Ideogram4PromptBuilderKJ", step: 8, min: 8, max: 16384 },
];

function calcDims(aspectRatio, megapixels, step, min, max) {
  const [wRatio, hRatio] = ASPECT_RATIOS[aspectRatio] || [1, 1];
  const totalPixels = megapixels * 1024 * 1024;
  const scale = Math.sqrt(totalPixels / (wRatio * hRatio));
  const clamp = (v) => Math.min(max, Math.max(min, Math.round(v / step) * step));
  let width = clamp(wRatio * scale);
  let height = clamp(hRatio * scale);
  return [width, height];
}

app.registerExtension({
  name: "ResolutionSync.Ideogram4",
  nodeCreated(node) {
    if (node.comfyClass === "ResolutionSelector") {
      const arW = node.widgets.find(w => w.name === "aspect_ratio");
      const mpW = node.widgets.find(w => w.name === "megapixels");

      const pushToTarget = () => {
        if (!arW || !mpW) return;
        for (const { comfyClass, step, min, max } of TARGET_NODE_TYPES) {
          const target = app.graph._nodes.find(n => n.comfyClass === comfyClass);
          if (!target) continue;
          const [width, height] = calcDims(arW.value, mpW.value, step, min, max);
          const tw = target.widgets.find(w => w.name === "width");
          const th = target.widgets.find(w => w.name === "height");

          if (tw) {
            tw.value = width;
            tw.callback?.(width, app.canvas, target, undefined, undefined);
          }
          if (th) {
            th.value = height;
            th.callback?.(height, app.canvas, target, undefined, undefined);
          }

          target.setDirtyCanvas(true, true);
        }
      };

      if (arW) { const orig = arW.callback; arW.callback = (v) => { orig?.(v); pushToTarget(); }; }
      if (mpW) { const orig = mpW.callback; mpW.callback = (v) => { orig?.(v); pushToTarget(); }; }
    }
  },
});