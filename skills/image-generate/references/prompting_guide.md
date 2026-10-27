# Master Prompt Engineering Guide

This guide provides the master-level prompt engineering framework utilized by the `image generate using coding` skill (`/image-generate`).

---

## 1. Universal Prompt Architecture

Every high-fidelity generation prompt is synthesized using the **10-Vector Prompt Formula**:

```
[Subject & Identity] + [Action / Pose / State] + [Environment & Context] + 
[Composition & Camera Angle] + [Lighting & Optics] + [Materials & Textures] + 
[Color Palette & Mood] + [Artistic / Photorealistic Style] + [Technical Constraints & Aspect Ratio] + 
[Negative Avoidance Rules]
```

---

## 2. Genre-Specific Prompt Engineering

### A. Photorealistic & Cinematic Imagery
*   **Optics & Camera:** Specify real optical hardware rather than generic buzzwords.
    *   *Examples:* `Shot on Hasselblad H6D-100c`, `50mm f/1.4 prime lens`, `35mm anamorphic widescreen lens`, `shallow depth of field with creamy optical bokeh`, `tactile lens falloff`.
*   **Lighting Physics:** Detail physical light sources, direction, and interaction.
    *   *Examples:* `Warm late afternoon golden hour directional rim lighting`, `soft diffused overcast daylight`, `subtle volumetric mist catching amber sunbeams`, `physically accurate ambient occlusion and specular highlights`.
*   **Surface Realism:** Micro-textures and material physics.
    *   *Examples:* `Subtle subsurface scattering on skin`, `authentic skin pores and fine vellus hair`, `tactile micro-scratches on anodized aluminum`, `realistic moisture condensation droplets on chilled glass`.
*   **Composition:** `Cinematic rule of thirds`, `low-angle perspective conveying scale`, `wide establishing shot`, `eye-level intimate close-up`.

### B. High-End Commercial Product Photography
*   **Environment:** Minimalist luxury setting, neutral textured concrete plinth, matte ceramic slab, or infinite cyclorama studio backdrop.
*   **Lighting:** `Professional three-point studio lighting setup`, `large overhead softbox creating smooth gradient reflections`, `dual edge-defining white rim lights`, `gentle neutral ground shadow`.
*   **Angle & Presentation:** `Hero product angle 30-degree elevation`, `front-facing centered symmetry`, `extreme macro close-up showcasing luxury watch escapement or cosmetic serum viscosity`.

### C. Technology, Agriculture & Science Visuals
*   **Smart Agriculture:** `Autonomous AI agricultural drone hovering over lush emerald green crop rows at sunrise`, `integrated multispectral LiDAR scanner emitting faint translucent telemetry guides`, `dew-covered foliage with photorealistic soil moisture textures`.
*   **Scientific & Medical:** `Bioluminescent cellular structures under confocal fluorescence microscopy`, `ultra-clean modern semiconductor cleanroom with robotic wafer handling arms`, `crisp optical fidelity`.

### D. Vector Graphics, Logos & Badges
*   **Styling Directives:** Do **not** use photorealistic terms for vector artwork.
*   **Keywords:** `Clean modern flat 2D vector graphic`, `crisp geometric contours`, `balanced negative space`, `bold minimalist iconography`, `SVG vector art style`, `no gradients or drop shadows` (or `smooth modern duotone gradient fill`), `centered on solid white background`.

---

## 3. Aspect Ratio Matrix

| Aspect Ratio | Common Standard | Best Use Cases |
| :--- | :--- | :--- |
| `1:1` | Square (1024x1024) | Product thumbnails, social avatars, vector badges, logos |
| `16:9` | Widescreen (1024x576) | Cinematic hero banners, desktop wallpapers, landscape vistas |
| `9:16` | Vertical (576x1024) | Mobile stories, reels, full-screen mobile splash screens |
| `4:3` | Standard Presentation | Editorial photography, tech architecture diagrams, iPad views |
| `3:2` | Classic 35mm DSLR | Professional portraiture, landscape photography, fine art |
| `2:3` | Classic Vertical DSLR | Full-length fashion portraits, vertical posters |

---

## 4. Unwanted Artifact Avoidance (Negative Directives)

To ensure master-level visual clarity, explicitly formulate prompt constraints that suppress common neural synthesis artifacts:

*   **Anatomy:** `No distorted hands, no missing or extra fingers, no unnatural joint angles, no plastic or airbrushed waxy skin.`
*   **Geometry:** `No warped architecture, no distorted circular geometry, no melted objects, no floating unattached elements.`
*   **Text & Logos:** `No random garbled pseudo-text, no unwanted gibberish letters, no accidental digital watermarks, no copyright stamps.`
*   **Composition:** `No awkward object cropping, no excessive chromatic aberration, no oversaturated blown-out highlights, no muddy shadows.`
