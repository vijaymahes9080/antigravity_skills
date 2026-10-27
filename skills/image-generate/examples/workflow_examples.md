# Workflow Examples: End-to-End Walkthroughs

This document illustrates practical command sequences and execution patterns for the `image generate using coding` skill (`/image-generate`).

---

## Example 1: Photorealistic Image Generation with Auto-Improvement

**User Prompt:**
> `/image-generate Create a photorealistic cinematic smart agriculture image and improve it automatically.`

**Step-by-Step Execution Plan:**
1.  **Formulate Master Prompt:**
    ```
    Cinematic ultra-realistic smart agriculture scene at sunrise. An autonomous agricultural drone with carbon-fiber frame and precision sensors hovers silently over geometric emerald-green tea plantation terraces. Morning mist weaves between misty hill contours as warm golden sunlight cuts through the valley. Dew drops glisten on lush foliage. Shot on Hasselblad H6D-100c, 50mm f/1.4 lens, shallow depth of field, creamy bokeh, physically plausible light scattering, 8k resolution, authentic textures. No distorted geometry, no cartoon artifacts, no watermarks.
    ```
2.  **Generate Image:**
    Invoke `generate_image` tool with:
    *   `Prompt`: Formulated prompt above.
    *   `ImageName`: `smart_agri_drone`
    *   `AspectRatio`: `16:9`
3.  **Inspect Programmatically & Visually:**
    *   Run `python scripts/engine.py inspect <path_to_artifact.png>` to verify file structure, dimensions, and dynamic range.
    *   View image with `view_file` to evaluate subject fidelity, anatomy, and lighting.
4.  **Automatic Improvement Loop:**
    *   Evaluate against the 100-point rubric.
    *   If contrast or dynamic range can be elevated, run:
        ```bash
        python scripts/engine.py improve <artifact.png> <improved.png> --contrast 1.08 --sharpness 1.12
        ```
5.  **Multi-Format Export & Verification:**
    ```bash
    python scripts/engine.py export-all <improved.png> ./dist/smart_agriculture_drone
    ```
6.  **Report Results:**
    Present the output paths (`.png`, `.jpg`, `.jpeg`), dimensions, quality score (e.g. 94/100), and verified file signatures.

---

## Example 2: Premium Product Advertisement with All Formats

**User Prompt:**
> `/image-generate Generate a premium product advertisement and export PNG, JPG, JPEG, and SVG where appropriate.`

**Step-by-Step Execution Plan:**
1.  **Prompt Construction:**
    *   Subject: Luxury minimalist frosted glass fragrance bottle with rose gold atomizing cap.
    *   Backdrop: Floating on dark obsidian marble water ripple surface, dual rim light highlights.
2.  **Generate Image:**
    *   Invoke `generate_image` tool with `AspectRatio: "1:1"`.
3.  **Export & Package:**
    *   Run `python scripts/engine.py export-all <fragrance.png> ./dist/luxury_perfume`.
    *   Verify generated `.png`, `.jpg`, and `.jpeg` files.
    *   Explain that because the product shot is a photograph, genuine SVG vector representation is not suitable, but all raster formats have been verified.

---

## Example 3: SVG Vector Graphic Creation & Multi-Format Render

**User Prompt:**
> `/image-generate Generate a high-tech cloud architecture diagram SVG and export high-res PNG and JPG.`

**Step-by-Step Execution Plan:**
1.  **Generate Clean SVG:**
    Run:
    ```bash
    python scripts/engine.py generate-vector --style architecture-diagram --title "Edge AI Ingestion Pipeline" --subtitle "Distributed Telemetry & Stream Analysis" --output ./diagram.svg --width 800 --height 500
    ```
2.  **Verify SVG Integrity:**
    ```bash
    python scripts/engine.py inspect ./diagram.svg
    ```
3.  **Export Multi-Format Suite:**
    ```bash
    python scripts/engine.py export-all ./diagram.svg ./dist/cloud_architecture
    ```
4.  **Confirm Decodability & Quality:**
    Verify that `cloud_architecture.svg`, `cloud_architecture.png`, `cloud_architecture.jpg`, and `cloud_architecture.jpeg` are all valid.

---

## Example 4: Existing Image Analysis & Defect Correction

**User Prompt:**
> `/image-generate Analyze ./input/product.png, correct visible defects, and preserve the original.`

**Step-by-Step Execution Plan:**
1.  **Preserve Source:** Do not modify `./input/product.png`.
2.  **Inspect:**
    ```bash
    python scripts/engine.py inspect ./input/product.png --json
    ```
3.  **Improve:**
    Apply needed corrections (e.g. contrast boost, white background composite):
    ```bash
    python scripts/engine.py improve ./input/product.png ./output/product_enhanced.png --contrast 1.1 --sharpness 1.15 --solid-bg "#FFFFFF"
    ```
4.  **Re-Inspect & Verify:**
    ```bash
    python scripts/engine.py inspect ./output/product_enhanced.png
    ```
5.  **Deliver Artifacts:** Return comparison report and verified output paths.
