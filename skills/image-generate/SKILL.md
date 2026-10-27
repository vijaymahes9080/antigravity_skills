---
name: image-generate
description: Professional AI image generation, programmatic graphics, multi-format conversion, and quality engineering workflow named "image generate using coding". Strictly adheres to zero-local-installation policy (no model weight downloads, no package installations). Supports native Antigravity tools, free hosted inference, SVG-to-PNG rasterization, WebP, raster-in-svg honesty, and automated validation.
---

# image generate using coding

A professional, production-minded Antigravity skill providing end-to-end AI image synthesis, algorithmic vector graphics, multi-format conversion, visual inspection, automated defect improvement, and export verification.

- **Preferred Slash Invocation:** `/image-generate`
- **Human-Readable Skill Name:** `image generate using coding`
- **Supporting Engine:** [engine.py](./scripts/engine.py)
- **Automated Test Suite:** [test_engine.py](./scripts/test_engine.py)
- **Zero-Installation Guarantee:** Modifies skill code only. Never downloads AI model weights, never installs pip/npm packages, and never creates persistent background servers.

---

## 1. Core Workflow Architecture

Whenever invoked via `/image-generate` or natural-language request:

```
[User Request / Natural-Language Prompt]
   │
   ├──> [1. Prompt Interpretation & Visual Specification]
   │       ├── Extract Subject, Scene, Composition, Optics, Lighting
   │       └── Map Aspect Ratio (1:1, 16:9, 9:16, 4:3, 3:2, 2:3)
   │
   ├──> [2. Provider Discovery & Prioritized Selection]
   │       ├── Priority A: Native Antigravity Tool (`generate_image`)
   │       ├── Priority B: Free Hosted Provider (Pollinations.ai / FLUX / SD Turbo)
   │       └── Priority C: Pre-Existing Local Runtime (ComfyUI / Ollama - if already active)
   │
   ├──> [3. Real AI Synthesis Execution]
   │       ├── Online/Native generation with bounded retry & rate-limit handling
   │       └── Surgical watermark suppression (100% zero-watermark delivery)
   │
   ├──> [4. Integrity & Quality Inspection]
   │       ├── Magic bytes verification (PNG, JPEG, WebP, SVG)
   │       ├── Pillow decoding, dimension matching, mode & alpha integrity
   │       └── Visual inspection against 100-point rubric
   │
   ├──> [5. Optional Programmatic Enhancement & Defect Repair]
   │       └── Histogram equalization, contrast, sharpness, solid background composite
   │
   ├──> [6. Multi-Format Packaging & Delivery]
   │       ├── Lossless PNG (primary)
   │       ├── Web-optimized WebP
   │       ├── Web-standard JPG / JPEG (solid composited background)
   │       └── SVG (genuine vector paths or transparently labeled raster containers)
   │
   └──> [7. Verified Asset Delivery & Technical Reporting]
```

---

## 2. Provider Adapter Architecture (Zero Local Installation)

The skill enforces a multi-tier provider adapter layer. You can inspect active providers anytime via:

```bash
python "<SKILL_DIR>/scripts/engine.py" providers
```

### Priority A — Native Antigravity Tool (`generate_image`)
* **Execution:** Direct conversational tool call inside Antigravity agent sessions.
* **Backend:** Google Gemini / Imagen models.
* **Authentication:** Handled automatically by the Antigravity agent runtime.
* **Cost / Quota:** Included in standard session quota; zero extra charges or API keys required.
* **Output:** Saved directly into conversation artifacts directory.

### Priority B — Free Hosted Image Generation (`pollinations`)
* **Execution:** Automated via `engine.py generate` or `engine.py generate-ai`.
* **Backend:** Open-weight FLUX / Stable Diffusion turbo inference nodes.
* **Authentication:** 100% Free public API; no account registration, no credit card, no API key.
* **License:** CreativeML Open RAIL-M / FLUX Schnell open weights.
* **Rate Limits & Resilience:** Free tier allows 1 image every 45s per IP. The engine parses the `Retry after Xs` cooldown, automatically sleeps for short delays (<= 15s) and retries, or transparently reports the remaining cooldown window.
* **Watermark Filtering:** Built-in surgical crop suppresses corner stamps with zero aspect ratio loss.

### Priority C — Pre-Existing Local Runtime (`local-runtime`)
* **Execution:** Checks if local inference server is ALREADY running on loopback ports:
  - ComfyUI: `http://127.0.0.1:8188`
  - Ollama: `http://127.0.0.1:11434`
* **Zero-Install Policy:** If no server is running, the engine cleanly reports `[UNAVAILABLE]`. It **strictly does not** download multi-gigabyte models, install Docker, or modify system packages.

---

## 3. CLI Commands & Usage Patterns

All operations are executed via the self-contained script engine:

### 1. Unified AI Image Generation
```bash
# Auto-detect best provider, generate 16:9 cinematic image
python "<SKILL_DIR>/scripts/engine.py" generate \
  --prompt "Autonomous AI agricultural drone hovering over lush emerald crop rows at golden hour, Hasselblad 50mm f/1.4" \
  --output ./generated_drone.png \
  --aspect-ratio 16:9 \
  --provider auto

# Generate 1:1 square asset with specific seed
python "<SKILL_DIR>/scripts/engine.py" generate \
  --prompt "Minimalist frosted glass perfume bottle on obsidian marble, dramatic studio lighting" \
  --output ./perfume.png \
  --aspect-ratio 1:1 \
  --seed 4242
```

### 2. Provider Discovery & Status Check
```bash
python "<SKILL_DIR>/scripts/engine.py" providers [--json]
```

### 3. Programmatic Inspection & Validation
```bash
python "<SKILL_DIR>/scripts/engine.py" inspect ./image.png [--json]
```
Verifies:
* File existence and non-zero byte size.
* Magic byte header signatures (`89 50 4E 47` for PNG, `FF D8 FF` for JPEG, `RIFF...WEBP` for WebP, `<svg>` XML root).
* Decodability with Pillow without corruption.
* Width, height, aspect ratio, mode (`RGB` vs `RGBA`), and alpha transparency.
* Watermark/embedded raster notices.

### 4. High-Fidelity SVG-to-Raster Conversion (Headless Chrome/Edge)
```bash
# Render SVG to transparent PNG with 2x scale
python "<SKILL_DIR>/scripts/engine.py" svg2raster ./vector.svg ./output_2x.png --scale 2.0

# Render SVG directly to WebP
python "<SKILL_DIR>/scripts/engine.py" svg2raster ./vector.svg ./output.webp --scale 1.5
```

### 5. Multi-Format Bundle Export
```bash
# Packages into .png, .jpg, .jpeg, .webp, and .svg (if vector)
python "<SKILL_DIR>/scripts/engine.py" export-all ./input_asset.png ./dist/final_bundle
```

### 6. Transparent Raster-to-SVG Wrapper (Vector Honesty)
```bash
# Wraps raster inside an SVG container with clear honesty disclaimer
python "<SKILL_DIR>/scripts/engine.py" embed-svg ./photo.png ./photo_wrapped.svg
```

### 7. Programmatic Image Improvement
```bash
python "<SKILL_DIR>/scripts/engine.py" improve ./input.png ./enhanced.png \
  --contrast 1.08 \
  --sharpness 1.15 \
  --solid-bg "#FFFFFF"
```

### 8. Algorithmic SVG Generation
```bash
python "<SKILL_DIR>/scripts/engine.py" generate-vector \
  --style tech-badge \
  --title "Antigravity Pipeline" \
  --subtitle "Zero-Install AI Synthesis" \
  --output ./badge.svg
```

---

## 4. Master Prompt Engineering Protocol

Formulate all generation prompts using the **10-Vector Prompt Formula**:

1. **Subject & Core Identity:** Explicit subject definition, physical materials, geometry.
2. **Action / Pose / State:** Dynamic pose, mechanical operation, or resting angle.
3. **Environment & Context:** Surroundings, background depth, atmospheric conditions.
4. **Composition & Optics:** Specific camera hardware (`Hasselblad H6D-100c`, `50mm f/1.4 prime`), angle of view, focal depth.
5. **Lighting Physics:** Key light, rim light, ambient occlusion, specular highlights.
6. **Materials & Micro-Textures:** Subsurface scattering, brushed metal, woven fabric.
7. **Color Palette & Tone:** Tailored palette, calibrated color temperature (e.g. 5200K daylight).
8. **Artistic / Photorealistic Direction:** Realistic photographic rendering vs clean 2D vector.
9. **Aspect Ratio & Compositional Framing:** Rule of thirds, centered symmetry, leading lines.
10. **Negative Avoidance Directives:** Suppress deformities, melted geometry, garbled text, and unwanted watermarks.

*Detailed reference:* [prompting_guide.md](./references/prompting_guide.md)

---

## 5. Aspect Ratio Presets

| Preset | Target Dimensions | Primary Use Cases |
| :--- | :--- | :--- |
| `1:1` | 1024 x 1024 | Product shots, social avatars, logos, square badges |
| `16:9` | 1024 x 576 | Landscape hero banners, cinematic scenes, wallpapers |
| `9:16` | 576 x 1024 | Mobile stories, vertical splash screens, portrait posters |
| `4:3` | 1024 x 768 | Editorial photography, presentation slides, diagrams |
| `3:2` | 1024 x 682 | Classic 35mm DSLR photography, fine art |
| `2:3` | 682 x 1024 | Vertical fashion portraiture, book covers |
| `21:9` | 1024 x 440 | Ultra-widescreen cinematic banners |

---

## 6. Raster vs. Vector Honesty Rules

1. **Photographic & Complex Images:**
   * Genuine AI image generation models output raster pixels (PNG/JPEG/WebP).
   * Never embed a base64 raster into an `<svg>` and falsely claim it is a "vectorized illustration".
   * If a user requests an SVG format for a raster image, generate `embed-svg` which explicitly includes a human-readable and machine-readable disclaimer:
     ```xml
     <!-- NOTICE: This SVG contains an embedded raster image. It is NOT a scalable vector path. -->
     ```
2. **Pure Vector Illustrations:**
   * For logos, icons, technical diagrams, and badges, generate clean, standard-compliant SVG code with native `<path>`, `<circle>`, `<polygon>`, and `<defs>` elements.
   * Author SVGs using [svg_guidelines.md](./references/svg_guidelines.md) or `generate-vector`.

---

## 7. Quality, Security & Non-Destructive Operation

* **Non-Destructive File Writing:** Output paths are checked via `get_safe_output_path`. If a file already exists and `--overwrite` is not passed, an incremented filename (e.g. `image_1.png`) is used. Existing user files are never deleted or silently overwritten.
* **Security & XML Sanitization:** All SVGs are sanitized before rasterization. Executable constructs (`<script>`, `javascript:`, `<foreignObject>`) are strictly rejected.
* **Zero Secret Exposure:** No `.env` files or API secrets are stored, inspected, or logged.
* **Output Validation:** Every generated artifact is validated with magic bytes, PIL decodability, non-zero byte size, and dimension verification before declaring success.

---

## 8. Verification & Test Suite

The skill includes a dedicated 15-test unit and integration test suite:

```bash
python -m unittest scripts/test_engine.py -v
```

### Test Coverage:
* `TestProviderArchitecture`: Tests provider discovery, metadata completeness, unavailable local runtime handling, and prioritization.
* `TestAspectRatiosAndSafety`: Tests aspect ratio math, custom ratio scaling, and collision-free file naming.
* `TestImageInspectionAndValidation`: Tests rejection of non-existent, empty (0-byte), and header-corrupted files.
* `TestSVGAndVectorHandling`: Tests SVG sanitization security, headless Chrome SVG-to-PNG rendering, and raster-in-SVG wrapper honesty detection.
* `TestMultiFormatPackaging`: Tests full export bundle generation (.png, .jpg, .jpeg, .webp) and format validation.
* `TestMockedProviderGeneration`: Deterministic unit tests with mocked network responses verifying watermark cropping, Pillow resizing, and 402 rate limit reporting.
* `TestLiveGenerationPipeline`: Live end-to-end integration test with the verified free hosted provider, validating actual generated PNG bytes.

---

## 9. Comprehensive Reference Library

* Master Prompting Guide: [prompting_guide.md](./references/prompting_guide.md)
* Quality Rubric & Improvement Protocol: [quality_rubric.md](./references/quality_rubric.md)
* SVG Standards & Security: [svg_guidelines.md](./references/svg_guidelines.md)
* Practical Workflow Examples: [workflow_examples.md](./examples/workflow_examples.md)
