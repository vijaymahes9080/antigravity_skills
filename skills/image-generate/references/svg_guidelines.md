# SVG Graphics, Security, and Raster-to-Vector Guidelines

This guide details best practices for authoring, validating, sanitizing, and converting SVG graphics within the `image generate using coding` skill (`/image-generate`).

---

## 1. Native SVG Construction Standards

When a user requests a logo, icon, badge, diagram, or vector illustration, generate clean, standard-compliant SVG code.

### Required Header & Attributes
*   Always include `xmlns="http://www.w3.org/2000/svg"`.
*   Always declare an explicit `viewBox` (e.g., `viewBox="0 0 800 600"`).
*   Declare default `width` and `height` corresponding to the viewBox coordinate space.
*   Use self-contained styling or SVG presentation attributes (`fill`, `stroke`, `stroke-width`).

### Structural Best Practices
*   **Defs & Gradients:** Place all `<linearGradient>`, `<radialGradient>`, `<pattern>`, and `<filter>` elements inside a `<defs>` block at the top of the file.
*   **Hierarchy:** Group related visual components into semantic `<g>` elements with descriptive `id` or `class` attributes.
*   **Cross-Platform Typography:** When rendering text, use system font stacks to ensure consistent rendering across operating systems:
    ```svg
    <text font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif" font-size="20" fill="#ffffff">Title</text>
    ```

---

## 2. Security & Sanitization Protocol

SVGs can technically embed executable JavaScript or external entities. Under the Antigravity Security Model:

1.  **Block Executable Elements:** Never include `<script>`, `<foreignObject>`, or `on*` event handlers (e.g., `onload`, `onclick`).
2.  **No External HTTP References:** Avoid `<image href="http://...">` or external stylesheet links that depend on network fetching. Keep all SVG graphics 100% self-contained.
3.  **Sanitization Check:** Run `engine.py inspect <file.svg>` before rendering untrusted SVGs. The engine uses defused XML parsing and pattern checks to reject dangerous constructs.

---

## 3. High-Fidelity SVG-to-Raster Conversion

SVGs are rasterized into PNG, JPG, JPEG, or WebP using `engine.py svg2raster`:

*   **Transparency Preservation:** Headless Chromium renders SVGs with a transparent canvas (`--default-background-color=00000000`).
*   **WebP & PNG Support:** Render directly to `.png` or optimized `.webp`:
    ```bash
    # Render at 2x resolution to PNG
    python scripts/engine.py svg2raster input.svg output_2x.png --scale 2.0

    # Render directly to WebP
    python scripts/engine.py svg2raster input.svg output.webp --scale 1.5
    ```
*   **JPEG Composition:** When converting SVG to JPG/JPEG, transparent areas are automatically composited onto a solid background (default `#FFFFFF`) to prevent black square artifacts.

---

## 4. Raster-to-Vector Honesty Rules

When a user provides a photograph or complex raster image and requests an SVG:

*   **Never Misrepresent:** Do **not** simply wrap a raster PNG/JPEG inside an `<svg><image href="data:image/png;base64,..."/></svg>` tag and claim it is a genuine vectorized photograph.
*   **Explicit Container Wrapper:** If an SVG container is explicitly required for a raster asset, generate it via:
    ```bash
    python scripts/engine.py embed-svg input.png output_wrapper.svg
    ```
    This embeds an explicit comment and metadata label documenting that the file is an SVG wrapper around a raster image, NOT a scalable vector path.
*   **Vectorization Limits & Zero-Installation Policy:** Photographic textures cannot be represented natively as clean scalable vector paths without severe loss of detail or generating gigabytes of polygon meshes. Under the Zero Local Installation policy, heavy third-party autotrace binaries are not installed. For logos and icons, author clean geometric SVG code natively.
