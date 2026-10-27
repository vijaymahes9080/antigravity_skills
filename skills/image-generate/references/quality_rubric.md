# Master Quality Scoring Rubric & Automatic Improvement Loop

This document specifies the evaluation criteria, scoring mechanics, and automated defect correction protocols for the `image generate using coding` skill (`/image-generate`).

---

## 1. The 100-Point Master Evaluation Rubric

Every generated or processed image is systematically evaluated across seven core dimensions:

| Category | Max Points | Evaluation Scope |
| :--- | :---: | :--- |
| **1. Request & Subject Fidelity** | 25 | Accurate representation of the user prompt, required subject matter, requested environment, props, and actions without omission or hallucinations. |
| **2. Realism or Style Consistency** | 20 | Adherence to requested aesthetic (photorealistic optical accuracy vs. flat vector minimalism vs. cinematic grade). Consistent physical behavior. |
| **3. Composition & Visual Hierarchy** | 15 | Rule of thirds, framing balance, focal point isolation, leading lines, headroom, and absence of awkward cropping. |
| **4. Technical Rendering Quality** | 15 | Sharpness, absence of blur or compression artifacts, crisp edges, accurate resolution, and absence of neural hallucinations (warped structures, floating objects). |
| **5. Lighting, Color & Materials** | 10 | Physically plausible light direction, specular highlights, soft contact shadows, coherent color temperature, and tactile material textures. |
| **6. Typography & Zero-Watermark Compliance** | 10 | Legibility and correct spelling of requested text, accurate micro-details, and 100% absence of unwanted watermarks, logos, or vendor stamps. |
| **7. Export Integrity** | 5 | Valid file format headers (magic bytes), decodable file structure, non-zero file size, and preservation of requested aspect ratio. |
| **TOTAL** | **100** | **Target Score: $\ge$ 90/100** |

*Note: For artwork without text, typography points (10 pts) are redistributed proportionally to Subject Fidelity (+5) and Technical Rendering (+5).*

---

## 2. Automated Quality Inspection Layers

Evaluation combines both **Programmatic Verification** and **Visual Inspection**:

### Layer 1: Programmatic Verification (`scripts/engine.py inspect`)
*   **File Existence & Non-Zero Byte Size**: Eliminates corrupted or interrupted writes.
*   **Binary Magic Byte Check**:
    *   PNG: `89 50 4E 47 0D 0A 1A 0A`
    *   JPEG: `FF D8 FF`
    *   SVG: Validated XML well-formedness with root `<svg>` tag.
*   **Dimension & Aspect Ratio Conformance**: Verifies pixels match requested specifications.
*   **Color Mode & Alpha Integrity**: Detects `RGBA` transparency, checks min/max alpha values, checks mean brightness and contrast standard deviation.

### Layer 2: Visual Inspection (`view_file` or Vision Model)
*   Subject presence, emotional tone, anatomical correctness.
*   Perspective convergence lines and horizon consistency.
*   Text legibility and artifact absence.

---

## 3. The 8-Stage Automatic Image Improvement Loop

When an image scores below 90/100 or exhibits visible defects, follow this structured loop:

```
[GENERATE] 
   └──> [INSPECT] 
           └──> [IDENTIFY DEFECTS] 
                   └──> [PRIORITIZE] 
                           └──> [IMPROVE] 
                                   └──> [RE-INSPECT] 
                                           └──> [EXPORT] 
                                                   └──> [VERIFY]
```

### Defect Classification & Remediation Strategies

| Severity | Defect Examples | Primary Remediation Action |
| :--- | :--- | :--- |
| **P0 - Critical** | Severe anatomical distortion, completely incorrect subject, corrupt file, illegible garbled text. | Prompt re-synthesis with enhanced negative constraints, seed variation, or programmatic SVG text overlay. |
| **P1 - Major** | Muddy lighting, washed-out low contrast, improper cropping, unwanted background artifacts. | Programmatic PIL adjustment (`engine.py improve`), reference-image editing with `ImagePaths`, or crop adjustment. |
| **P2 - Minor** | Slight softness, border padding needed, white background requirement for transparent PNG. | PIL sharpness boost (`sharpness=1.15`), autocontrast histogram stretch, or solid background composition. |

### Improvement Rules:
1.  **Maximum Iterations:** Run up to **3 improvement rounds**. If criteria are met early ($\ge 90$), stop immediately.
2.  **Surgical Changes:** Preserve all correct portions of the image; do not perform indiscriminate full regenerations for minor color/contrast flaws.
3.  **Honest Verification:** Never claim a defect was fixed without re-inspecting the updated output file.
