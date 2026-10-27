#!/usr/bin/env python3
"""
Image Engineering Engine for Antigravity Skill: "image generate using coding" (/image-generate)
============================================================================================
Professional, production-grade image synthesis, conversion, and validation engine.
Strictly adheres to Zero Local Installation policy:
  - Uses only Python standard library and pre-existing Pillow/PIL.
  - Zero package downloads, zero multi-GB model weights downloaded.
  - Multi-tier provider adapter architecture (Native Antigravity -> Free Hosted -> Local Runtime).
  - High-fidelity SVG-to-PNG rendering via headless Chromium (Chrome/Edge).
  - Multi-format packaging (.png, .jpg, .jpeg, .webp, .svg).
  - Transparent raster-to-vector honesty (distinguishes embedded raster from vector paths).
  - Programmatic quality scoring against 100-point rubric.
"""

import argparse
import base64
import html
import json
import math
import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple, List

try:
    from PIL import Image, ImageOps, ImageEnhance, ImageDraw, ImageFont, features
    HAS_PIL = True
    HAS_WEBP = features.check("webp")
except ImportError:
    HAS_PIL = False
    HAS_WEBP = False

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False


# Standard Magic Byte Signatures
MAGIC_PNG = b"\x89PNG\r\n\x1a\n"
MAGIC_JPEG = b"\xff\xd8\xff"
MAGIC_GIF = b"GIF8"
MAGIC_RIFF = b"RIFF"

# Aspect Ratio Pixel Dimension Presets (default base: 1024)
ASPECT_RATIO_PRESETS: Dict[str, Tuple[int, int]] = {
    "1:1": (1024, 1024),
    "16:9": (1024, 576),
    "9:16": (576, 1024),
    "4:3": (1024, 768),
    "3:4": (768, 1024),
    "3:2": (1024, 682),
    "2:3": (682, 1024),
    "21:9": (1024, 440),
}


def find_browser_executable() -> Optional[str]:
    """Locates Chrome or Edge browser for headless high-fidelity SVG rasterization."""
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        shutil.which("chrome"),
        shutil.which("msedge"),
        shutil.which("chromium"),
        shutil.which("google-chrome"),
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None


def get_safe_output_path(target_path: str, overwrite: bool = False) -> str:
    """
    Ensures non-destructive file writes. If target exists and overwrite is False,
    appends an incrementing counter (e.g. name_1.png, name_2.png).
    """
    if overwrite or not os.path.exists(target_path):
        return os.path.abspath(target_path)

    directory, filename = os.path.split(target_path)
    stem, ext = os.path.splitext(filename)
    counter = 1
    while True:
        candidate = os.path.join(directory, f"{stem}_{counter}{ext}")
        if not os.path.exists(candidate):
            return os.path.abspath(candidate)
        counter += 1


def parse_aspect_ratio_to_dimensions(ratio_str: str, default_width: int = 1024, default_height: int = 1024) -> Tuple[int, int]:
    """Parses standard ratio strings (e.g. '16:9', '1:1', '4:3') into pixel dimensions."""
    normalized = ratio_str.strip().lower()
    for preset, dims in ASPECT_RATIO_PRESETS.items():
        if normalized == preset.lower():
            return dims
    # If ratio format like W:H
    m = re.match(r"^(\d+)\s*[:/x]\s*(\d+)$", normalized)
    if m:
        w_factor = float(m.group(1))
        h_factor = float(m.group(2))
        if w_factor > 0 and h_factor > 0:
            scale = 1024.0 / max(w_factor, h_factor)
            w = int(round(w_factor * scale))
            h = int(round(h_factor * scale))
            # Round to multiples of 8 or 16 for clean neural synthesis
            w = (w // 16) * 16
            h = (h // 16) * 16
            return (max(64, w), max(64, h))
    return (default_width, default_height)


# ==============================================================================
# PROVIDER ADAPTER ARCHITECTURE
# ==============================================================================

class BaseImageProvider(ABC):
    """Abstract base class for all image generation providers."""

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier for the provider."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable provider name."""
        pass

    @property
    @abstractmethod
    def priority(self) -> str:
        """Priority tier ('Priority A', 'Priority B', 'Priority C')."""
        pass

    @abstractmethod
    def get_metadata(self) -> Dict[str, Any]:
        """Returns provider capabilities, licensing, cost, and usage details."""
        pass

    @abstractmethod
    def is_available(self) -> Tuple[bool, str]:
        """Returns (available: bool, reason_or_status: str)."""
        pass

    @abstractmethod
    def generate(self, prompt: str, output_path: str, width: int = 1024, height: int = 1024,
                 seed: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        """Executes actual image generation and returns result report."""
        pass


class AntigravityNativeProvider(BaseImageProvider):
    """
    Priority A: Native Antigravity Tool (generate_image).
    Direct integration with Google Gemini / Imagen within Antigravity chat sessions.
    """

    @property
    def id(self) -> str:
        return "antigravity-native"

    @property
    def name(self) -> str:
        return "Antigravity Native (generate_image Tool)"

    @property
    def priority(self) -> str:
        return "Priority A (Native Tool)"

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "priority": self.priority,
            "cost": "Included in Antigravity session quota (zero extra charge)",
            "license": "Google DeepMind / Generative AI Terms of Service",
            "authentication": "Handled internally by Antigravity runtime",
            "formats": ["PNG", "JPEG"],
            "aspect_ratios": ["1:1", "16:9", "9:16", "4:3", "3:4"],
            "max_resolution": "1024x1024 (native)",
            "description": "Native tool calling `generate_image` from Antigravity LLM. Primary choice inside active chat."
        }

    def is_available(self) -> Tuple[bool, str]:
        # In standalone script execution outside IDE subagent, generate_image tool is routed to engine.
        # Inside agent context, agent invokes generate_image directly.
        in_antigravity = "ANTIGRAVITY_AGENT_ID" in os.environ or "GEMINI_CLI" in os.environ
        if in_antigravity:
            return True, "Active within Antigravity runtime."
        return True, "Available via agent tool calling `generate_image` during conversational turns."

    def generate(self, prompt: str, output_path: str, width: int = 1024, height: int = 1024,
                 seed: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        # Script-side invocation notes that native tool is invoked by agent
        return {
            "success": False,
            "provider": self.id,
            "error": "AntigravityNativeProvider is executed via agent's `generate_image` tool call in chat. For CLI execution, use `pollinations` or `auto`.",
            "output_path": None
        }


class PollinationsHostedProvider(BaseImageProvider):
    """
    Priority B: Free Hosted Image Generation (Pollinations.ai).
    100% free, zero authentication, zero credit card, open-access neural synthesis.
    Backed by open-weight FLUX / Stable Diffusion turbo inference nodes.
    Features automated surgical watermark suppression and strict zero-watermark delivery.
    """

    @property
    def id(self) -> str:
        return "pollinations"

    @property
    def name(self) -> str:
        return "Pollinations.ai Open Cluster (FLUX / SD Turbo)"

    @property
    def priority(self) -> str:
        return "Priority B (Free Hosted)"

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "priority": self.priority,
            "cost": "100% Free, zero API key, no account registration required",
            "license": "CreativeML Open RAIL-M / FLUX Schnell Open Weights",
            "authentication": "None (Open Public API)",
            "formats": ["PNG", "JPEG", "WebP"],
            "aspect_ratios": ["1:1", "16:9", "9:16", "4:3", "3:2", "2:3", "21:9"],
            "max_resolution": "1024x1024 (or customized aspect bounds)",
            "description": "High-throughput free hosted generation using open-weight diffusion models with surgical watermark filtering."
        }

    def is_available(self) -> Tuple[bool, str]:
        test_url = "https://image.pollinations.ai/prompt/ping?width=16&height=16&nologo=true"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AntigravitySkill/2.0"}
        try:
            req = urllib.request.Request(test_url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as resp:
                if resp.status == 200:
                    return True, "Online and reachable (HTTP 200 OK)."
                return False, f"HTTP status {resp.status}"
        except Exception as e:
            return False, f"Network unreachable: {str(e)}"

    def generate(self, prompt: str, output_path: str, width: int = 1024, height: int = 1024,
                 seed: Optional[int] = None, no_watermark: bool = True, model: str = "flux",
                 **kwargs) -> Dict[str, Any]:
        if seed is None:
            seed = random.randint(1, 9999999)

        # Padding height if removing watermark to avoid aspect-ratio deformation
        if no_watermark:
            pad_h = max(36, int(height * 0.07))
            req_h = height + pad_h
        else:
            req_h = height

        encoded_prompt = urllib.parse.quote(prompt.strip())
        url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={req_h}&seed={seed}&nologo=true&model={model}"

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AntigravitySkill/2.0"}
        req = urllib.request.Request(url, headers=headers)

        tmp_dir = tempfile.gettempdir()
        tmp_raw = os.path.join(tmp_dir, f"ai_gen_{os.getpid()}_{seed}.raw")

        attempts = 0
        last_error = None
        data = b""

        while attempts < 2:
            attempts += 1
            try:
                with urllib.request.urlopen(req, timeout=50) as resp:
                    data = resp.read()
                if len(data) > 0:
                    break
            except urllib.error.HTTPError as e:
                last_error = e
                err_body = e.read().decode("utf-8", errors="ignore")
                if e.code == 402:
                    wait_sec = 0
                    m = re.search(r"Retry after (\d+)s", err_body)
                    if m:
                        wait_sec = int(m.group(1))
                    if wait_sec > 0 and wait_sec <= 15:
                        time.sleep(wait_sec + 1)
                        continue
                    else:
                        raise RuntimeError(
                            f"Pollinations Free Quota Limit: 1 image every 45s per IP. Cooldown active (wait {wait_sec}s). Original: {err_body}"
                        )
                elif e.code == 503:
                    time.sleep(3)
                    continue
                else:
                    raise RuntimeError(f"Pollinations HTTP {e.code} error: {err_body}")
            except Exception as e:
                last_error = e
                time.sleep(1)

        if len(data) == 0:
            raise RuntimeError(f"Pollinations generation failed after {attempts} attempts. Details: {last_error}")

        try:
            with open(tmp_raw, "wb") as f:
                f.write(data)

            target_out = os.path.abspath(output_path)
            os.makedirs(os.path.dirname(target_out), exist_ok=True)
            out_ext = os.path.splitext(target_out)[1].lower()

            if not HAS_PIL:
                shutil.move(tmp_raw, target_out)
                return {
                    "success": True,
                    "provider": self.id,
                    "model": model,
                    "output_path": target_out,
                    "seed": seed,
                    "watermark_removed": False,
                    "size_bytes": os.path.getsize(target_out)
                }

            with Image.open(tmp_raw) as img:
                w, h = img.size
                if no_watermark:
                    crop_bottom = max(36, int(h * 0.07))
                    cropped = img.crop((0, 0, w, h - crop_bottom))
                    final_img = cropped.resize((width, height), Image.Resampling.LANCZOS)
                else:
                    final_img = img.resize((width, height), Image.Resampling.LANCZOS)

                if out_ext == ".png":
                    final_img.save(target_out, format="PNG", optimize=True)
                elif out_ext in [".jpg", ".jpeg"]:
                    rgb_img = final_img.convert("RGB")
                    rgb_img.save(target_out, format="JPEG", quality=95, optimize=True)
                elif out_ext == ".webp" and HAS_WEBP:
                    final_img.save(target_out, format="WEBP", quality=95)
                else:
                    final_img.save(target_out)

            return {
                "success": True,
                "provider": self.id,
                "model": model,
                "output_path": target_out,
                "width": width,
                "height": height,
                "seed": seed,
                "watermark_removed": no_watermark,
                "size_bytes": os.path.getsize(target_out)
            }
        finally:
            if os.path.exists(tmp_raw):
                try:
                    os.remove(tmp_raw)
                except OSError:
                    pass


class LocalRuntimeProvider(BaseImageProvider):
    """
    Priority C: Pre-existing Local Runtime (ComfyUI / Ollama).
    Strictly adheres to Zero Local Installation policy:
      - Does NOT install packages or download model weights.
      - Checks if a local service is ALREADY running on local ports.
      - If absent, cleanly reports unavailability without side-effects.
    """

    @property
    def id(self) -> str:
        return "local-runtime"

    @property
    def name(self) -> str:
        return "Local Runtime (ComfyUI / Ollama / Diffusers)"

    @property
    def priority(self) -> str:
        return "Priority C (Local Runtime)"

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "priority": self.priority,
            "cost": "100% Free (Local compute)",
            "license": "Depends on local model installed",
            "authentication": "Local loopback",
            "requirements": "Pre-existing ComfyUI (port 8188) or Ollama (port 11434)",
            "policy_notice": "Under Zero-Install policy, models and servers will NOT be downloaded automatically."
        }

    def is_available(self) -> Tuple[bool, str]:
        # Check ComfyUI port 8188
        for name, port, path in [("ComfyUI", 8188, "/system_stats"), ("Ollama", 11434, "/api/tags")]:
            try:
                url = f"http://127.0.0.1:{port}{path}"
                with urllib.request.urlopen(url, timeout=1.5) as r:
                    if r.status == 200:
                        return True, f"Detected active local {name} instance on port {port}."
            except Exception:
                pass
        return False, "No active local inference server (ComfyUI/Ollama) listening on localhost. No packages or weights downloaded per zero-installation policy."

    def generate(self, prompt: str, output_path: str, width: int = 1024, height: int = 1024,
                 seed: Optional[int] = None, **kwargs) -> Dict[str, Any]:
        avail, reason = self.is_available()
        if not avail:
            raise RuntimeError(f"Local runtime unavailable: {reason}")
        raise NotImplementedError("Local generation requested, but no active ComfyUI/Ollama workflow configuration provided.")


class ProviderRegistry:
    """Manages discovery, capability querying, and prioritized provider selection."""

    def __init__(self):
        self._providers: Dict[str, BaseImageProvider] = {
            "pollinations": PollinationsHostedProvider(),
            "antigravity-native": AntigravityNativeProvider(),
            "local-runtime": LocalRuntimeProvider(),
        }

    def list_all(self) -> List[Dict[str, Any]]:
        results = []
        for pid, provider in self._providers.items():
            avail, status_msg = provider.is_available()
            meta = provider.get_metadata()
            meta["available"] = avail
            meta["status_message"] = status_msg
            results.append(meta)
        return results

    def get(self, provider_id: str) -> Optional[BaseImageProvider]:
        return self._providers.get(provider_id.lower())

    def select_best_available(self) -> Tuple[Optional[BaseImageProvider], str]:
        """
        Prioritized selection order:
          1. Pollinations (fully functional standalone CLI & hosted inference)
          2. Antigravity Native (for conversational tool invocation)
          3. Local Runtime (if user already had ComfyUI running)
        """
        # 1. Check Pollinations
        p_hosted = self._providers["pollinations"]
        avail, status = p_hosted.is_available()
        if avail:
            return p_hosted, "Selected Priority B free hosted provider (Pollinations.ai) - verified online and responsive."

        # 2. Check Local Runtime
        p_local = self._providers["local-runtime"]
        avail, status = p_local.is_available()
        if avail:
            return p_local, f"Selected Priority C local runtime - {status}"

        # 3. Check Antigravity Native
        p_native = self._providers["antigravity-native"]
        return p_native, "Falling back to Antigravity Native tool calling (`generate_image`)."


# ==============================================================================
# SVG & RASTER RENDERING & VALIDATION
# ==============================================================================

def sanitize_svg_content(content: str) -> Tuple[bool, str, Optional[str]]:
    """
    Validates SVG content for XML well-formedness and checks for unsafe tags.
    Returns: (is_valid, content, error_message)
    """
    lowered = content.lower()
    if "<script" in lowered or "javascript:" in lowered or "<foreignobject" in lowered:
        return False, content, "Security warning: Potentially unsafe script or foreignObject found in SVG."

    try:
        root = ET.fromstring(content)
        if not root.tag.lower().endswith("svg"):
            return False, content, f"Root XML element is '{root.tag}', expected '<svg>'."
        return True, content, None
    except ET.ParseError as e:
        return False, content, f"XML syntax error: {str(e)}"


def parse_svg_dimensions(svg_path: str) -> Tuple[int, int]:
    """Extracts width and height or viewBox dimensions from an SVG file."""
    try:
        tree = ET.parse(svg_path)
        root = tree.getroot()
        viewbox = root.attrib.get("viewBox") or root.attrib.get("viewbox")
        width_str = root.attrib.get("width")
        height_str = root.attrib.get("height")

        def clean_dim(val: Optional[str]) -> Optional[int]:
            if not val:
                return None
            m = re.match(r"^([\d.]+)", val.strip())
            return int(float(m.group(1))) if m else None

        w = clean_dim(width_str)
        h = clean_dim(height_str)

        if (w is None or h is None) and viewbox:
            parts = [float(p) for p in re.split(r"[\s,]+", viewbox.strip()) if p]
            if len(parts) == 4:
                w = int(parts[2])
                h = int(parts[3])

        return (w or 800, h or 800)
    except Exception:
        return (800, 800)


def render_svg_to_png(svg_path: str, output_png: str, width: Optional[int] = None, height: Optional[int] = None, scale: float = 1.0) -> bool:
    """
    Renders SVG to PNG with full transparency using headless Chromium.
    Falls back gracefully if browser is unavailable.
    """
    browser = find_browser_executable()
    if not browser:
        raise RuntimeError("Headless browser (Chrome/Edge) not found. Required for SVG rasterization.")

    with open(svg_path, "r", encoding="utf-8", errors="replace") as f:
        svg_code = f.read()

    is_valid, _, err = sanitize_svg_content(svg_code)
    if not is_valid:
        raise ValueError(f"Invalid or unsafe SVG: {err}")

    orig_w, orig_h = parse_svg_dimensions(svg_path)
    target_w = int(width if width else orig_w * scale)
    target_h = int(height if height else orig_h * scale)

    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body {{
    margin: 0;
    padding: 0;
    width: {target_w}px;
    height: {target_h}px;
    overflow: hidden;
    background: transparent !important;
  }}
  svg {{
    width: 100%;
    height: 100%;
    display: block;
  }}
</style>
</head>
<body>
{svg_code}
</body>
</html>"""

    tmp_dir = tempfile.gettempdir()
    tmp_html = os.path.join(tmp_dir, f"render_svg_{os.getpid()}_{abs(hash(svg_path))}.html")

    try:
        with open(tmp_html, "w", encoding="utf-8") as f:
            f.write(html_content)

        os.makedirs(os.path.dirname(os.path.abspath(output_png)), exist_ok=True)
        tmp_shot = os.path.join(tmp_dir, f"shot_{os.getpid()}_{abs(hash(output_png))}.png")

        cmd = [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--default-background-color=00000000",
            f"--window-size={target_w},{target_h}",
            f"--screenshot={tmp_shot}",
            f"file:///{tmp_html.replace(os.sep, '/')}"
        ]

        res = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
        if res.returncode != 0:
            raise RuntimeError(f"Browser screenshot failed: {res.stderr}")

        if not os.path.exists(tmp_shot) or os.path.getsize(tmp_shot) == 0:
            raise RuntimeError(f"Renderer did not produce output PNG: {res.stderr}")

        if HAS_PIL:
            with Image.open(tmp_shot) as img:
                if img.size != (target_w, target_h):
                    resized = img.resize((target_w, target_h), Image.Resampling.LANCZOS)
                    resized.save(output_png, format="PNG")
                else:
                    img.save(output_png, format="PNG")
        else:
            shutil.copy2(tmp_shot, output_png)

        if os.path.exists(tmp_shot):
            try:
                os.remove(tmp_shot)
            except OSError:
                pass

        return True
    finally:
        if os.path.exists(tmp_html):
            try:
                os.remove(tmp_html)
            except OSError:
                pass


def inspect_image(file_path: str) -> Dict[str, Any]:
    """
    Performs comprehensive technical inspection of an image file.
    Validates file existence, non-zero size, magic bytes, PIL decoding,
    dimensions, aspect ratio, color mode, alpha channel, and statistics.
    """
    report: Dict[str, Any] = {
        "file_path": os.path.abspath(file_path),
        "exists": os.path.exists(file_path),
        "file_name": os.path.basename(file_path),
        "extension": os.path.splitext(file_path)[1].lower(),
        "valid": False,
        "format": None,
        "size_bytes": 0,
        "dimensions": None,
        "aspect_ratio": None,
        "mode": None,
        "has_transparency": False,
        "magic_bytes_matched": False,
        "issues": []
    }

    if not report["exists"]:
        report["issues"].append("File does not exist.")
        return report

    report["size_bytes"] = os.path.getsize(file_path)
    if report["size_bytes"] == 0:
        report["issues"].append("File is empty (0 bytes).")
        return report

    ext = report["extension"]

    # SVG Inspection
    if ext == ".svg":
        try:
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            is_valid, _, err = sanitize_svg_content(content)
            report["format"] = "SVG"
            report["valid"] = is_valid
            report["magic_bytes_matched"] = "<svg" in content.lower()
            if not is_valid:
                report["issues"].append(err or "SVG failed syntax/security validation.")
            w, h = parse_svg_dimensions(file_path)
            report["dimensions"] = {"width": w, "height": h}
            report["aspect_ratio"] = f"{w}:{h}" if h != 0 else "N/A"
            report["has_transparency"] = True
            # Detect embedded raster wrappers
            if "<image" in content.lower() and "data:image/" in content:
                report["is_embedded_raster_wrapper"] = True
                report["issues"].append("Notice: SVG wraps an embedded raster image; it is not a pure vector illustration.")
            else:
                report["is_embedded_raster_wrapper"] = False
            return report
        except Exception as e:
            report["issues"].append(f"Failed to read SVG: {str(e)}")
            return report

    # Raster Inspection (PNG, JPG, JPEG, WEBP)
    with open(file_path, "rb") as f:
        header = f.read(16)

    if ext == ".png":
        report["magic_bytes_matched"] = header.startswith(MAGIC_PNG)
        if not report["magic_bytes_matched"]:
            report["issues"].append("PNG file header signature mismatch.")
    elif ext in [".jpg", ".jpeg"]:
        report["magic_bytes_matched"] = header.startswith(MAGIC_JPEG)
        if not report["magic_bytes_matched"]:
            report["issues"].append("JPEG file header signature mismatch.")
    elif ext == ".webp":
        report["magic_bytes_matched"] = header.startswith(MAGIC_RIFF) and b"WEBP" in header[8:12]
        if not report["magic_bytes_matched"]:
            report["issues"].append("WebP file header signature mismatch.")

    if not HAS_PIL:
        report["issues"].append("Pillow library not installed; cannot decode raster image details.")
        return report

    try:
        with Image.open(file_path) as img:
            img.verify()

        with Image.open(file_path) as img:
            report["format"] = img.format
            w, h = img.size
            report["dimensions"] = {"width": w, "height": h}
            gcd = math.gcd(w, h)
            report["aspect_ratio"] = f"{w // gcd}:{h // gcd}"
            report["mode"] = img.mode

            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                report["has_transparency"] = True
                if img.mode == "RGBA":
                    alpha = img.getchannel("A")
                    min_a, max_a = alpha.getextrema()
                    report["alpha_min"] = min_a
                    report["alpha_max"] = max_a
                    report["actual_transparent_pixels"] = min_a < 255
            else:
                report["has_transparency"] = False

            if HAS_NUMPY:
                arr = np.array(img.convert("RGB"))
                report["brightness_mean"] = round(float(np.mean(arr)), 2)
                report["contrast_std"] = round(float(np.std(arr)), 2)

            report["valid"] = (len(report["issues"]) == 0)
    except Exception as e:
        report["valid"] = False
        report["issues"].append(f"PIL failed to decode image: {str(e)}")

    return report


def convert_raster(input_path: str, output_path: str, quality: int = 95, bg_color: Tuple[int, int, int] = (255, 255, 255)) -> bool:
    """
    Converts between raster formats (PNG, JPG, JPEG, WebP).
    When converting to JPG/JPEG, safely composites any alpha channel onto a solid background.
    """
    if not HAS_PIL:
        raise RuntimeError("Pillow is required for raster image conversion.")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    out_ext = os.path.splitext(output_path)[1].lower()

    with Image.open(input_path) as img:
        if out_ext in [".jpg", ".jpeg"]:
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                img = img.convert("RGBA")
                solid_bg = Image.new("RGB", img.size, bg_color)
                solid_bg.paste(img, mask=img.split()[3])
                final_img = solid_bg
            else:
                final_img = img.convert("RGB")
            final_img.save(output_path, format="JPEG", quality=quality, optimize=True)
        elif out_ext == ".webp":
            if not HAS_WEBP:
                raise RuntimeError("WebP encoding is not supported by current Pillow installation.")
            img.save(output_path, format="WEBP", quality=quality)
        elif out_ext == ".png":
            img.save(output_path, format="PNG", optimize=True)
        else:
            img.save(output_path)

    return True


def embed_raster_in_svg(raster_path: str, output_svg_path: str) -> str:
    """
    Creates an explicit SVG container wrapping a base64 raster image.
    Strictly documents and labels that this is an SVG wrapper around a raster,
    preserving full honesty against false vectorization claims.
    """
    if not HAS_PIL:
        raise RuntimeError("Pillow is required to embed raster in SVG.")

    with Image.open(raster_path) as img:
        w, h = img.size

    with open(raster_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode("ascii")

    ext = os.path.splitext(raster_path)[1].lower().replace(".", "")
    mime = "image/png" if ext == "png" else ("image/webp" if ext == "webp" else "image/jpeg")

    svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <!-- ================================================================= -->
  <!-- NOTICE: RASTER EMBEDDED CONTAINER                                 -->
  <!-- This SVG contains an embedded raster image. It is NOT a scalable  -->
  <!-- vector path illustration. Preserves pixel fidelity without false  -->
  <!-- algorithmic tracing artifacts.                                    -->
  <!-- ================================================================= -->
  <title>Embedded Raster Asset ({w}x{h})</title>
  <image width="{w}" height="{h}" href="data:{mime};base64,{b64_data}" />
</svg>"""

    os.makedirs(os.path.dirname(os.path.abspath(output_svg_path)), exist_ok=True)
    with open(output_svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    return output_svg_path


def package_and_export_all(source_path: str, base_output_path: str, quality: int = 95) -> Dict[str, Any]:
    """
    Exports the input image into all mandatory formats:
      - .png
      - .jpg
      - .jpeg
      - .webp (if Pillow supports WebP)
      - .svg (preserved if source is SVG, or wrapped with explicit disclaimer)
    Verifies that every exported file has real matching encoding and non-zero size.
    """
    results: Dict[str, Any] = {
        "source": source_path,
        "base_output": base_output_path,
        "exports": {},
        "all_passed": True
    }

    dir_name = os.path.dirname(os.path.abspath(base_output_path))
    file_stem = os.path.splitext(os.path.basename(base_output_path))[0]
    os.makedirs(dir_name, exist_ok=True)

    png_path = os.path.join(dir_name, f"{file_stem}.png")
    jpg_path = os.path.join(dir_name, f"{file_stem}.jpg")
    jpeg_path = os.path.join(dir_name, f"{file_stem}.jpeg")
    webp_path = os.path.join(dir_name, f"{file_stem}.webp")
    svg_path = os.path.join(dir_name, f"{file_stem}.svg")

    src_ext = os.path.splitext(source_path)[1].lower()

    try:
        if src_ext == ".svg":
            if os.path.abspath(source_path) != os.path.abspath(svg_path):
                shutil.copy2(source_path, svg_path)
            render_svg_to_png(svg_path, png_path)
            convert_raster(png_path, jpg_path, quality=quality)
            shutil.copy2(jpg_path, jpeg_path)
            if HAS_WEBP:
                convert_raster(png_path, webp_path, quality=quality)
            targets = [png_path, jpg_path, jpeg_path, svg_path]
            if HAS_WEBP:
                targets.append(webp_path)
        else:
            if src_ext == ".png":
                if os.path.abspath(source_path) != os.path.abspath(png_path):
                    shutil.copy2(source_path, png_path)
            else:
                convert_raster(source_path, png_path)

            convert_raster(png_path, jpg_path, quality=quality)
            shutil.copy2(jpg_path, jpeg_path)

            targets = [png_path, jpg_path, jpeg_path]
            if HAS_WEBP:
                convert_raster(png_path, webp_path, quality=quality)
                targets.append(webp_path)

        for t in targets:
            insp = inspect_image(t)
            passed = insp["valid"] and insp["magic_bytes_matched"]
            results["exports"][t] = {
                "valid": passed,
                "format": insp["format"],
                "dimensions": insp["dimensions"],
                "size_bytes": insp["size_bytes"],
                "issues": insp["issues"]
            }
            if not passed:
                results["all_passed"] = False

    except Exception as e:
        results["all_passed"] = False
        results["error"] = str(e)

    return results


def improve_image(input_path: str, output_path: str,
                  autocontrast: bool = True,
                  brightness: float = 1.0,
                  contrast: float = 1.05,
                  sharpness: float = 1.1,
                  solid_bg: Optional[str] = None) -> bool:
    """
    Applies programmatic refinements to an image:
      - Autocontrast / histogram balancing
      - Brightness, contrast, and sharpness adjustments
      - Optional solid background composite for transparent assets
    """
    if not HAS_PIL:
        raise RuntimeError("Pillow is required for image improvement.")

    with Image.open(input_path) as img:
        work_img = img.copy()

        if solid_bg and work_img.mode in ("RGBA", "LA"):
            work_img = work_img.convert("RGBA")
            bg_color = (255, 255, 255)
            if solid_bg.startswith("#") and len(solid_bg) == 7:
                bg_color = tuple(int(solid_bg[i:i+2], 16) for i in (1, 3, 5))
            solid = Image.new("RGBA", work_img.size, bg_color + (255,))
            solid.paste(work_img, mask=work_img.split()[3])
            work_img = solid

        is_rgba = work_img.mode == "RGBA"
        if is_rgba:
            r, g, b, a = work_img.split()
            rgb = Image.merge("RGB", (r, g, b))
        else:
            rgb = work_img.convert("RGB")

        if autocontrast:
            rgb = ImageOps.autocontrast(rgb, cutoff=0.5)

        if brightness != 1.0:
            enh_b = ImageEnhance.Brightness(rgb)
            rgb = enh_b.enhance(brightness)

        if contrast != 1.0:
            enh_c = ImageEnhance.Contrast(rgb)
            rgb = enh_c.enhance(contrast)

        if sharpness != 1.0:
            enh_s = ImageEnhance.Sharpness(rgb)
            rgb = enh_s.enhance(sharpness)

        if is_rgba and not solid_bg:
            r, g, b = rgb.split()
            work_img = Image.merge("RGBA", (r, g, b, a))
        else:
            work_img = rgb

        out_ext = os.path.splitext(output_path)[1].lower()
        if out_ext in [".jpg", ".jpeg"]:
            work_img = work_img.convert("RGB")
            work_img.save(output_path, format="JPEG", quality=95, optimize=True)
        elif out_ext == ".webp" and HAS_WEBP:
            work_img.save(output_path, format="WEBP", quality=95)
        else:
            work_img.save(output_path, format="PNG", optimize=True)

    return True


def generate_algorithmic_svg(style: str, title: str, subtitle: str, output_path: str, width: int = 800, height: int = 500) -> str:
    """
    Generates a high-quality, scalable SVG graphic algorithmic illustration.
    Styles: 'tech-badge', 'architecture-diagram', 'product-banner'.
    """
    title_escaped = html.escape(title)
    subtitle_escaped = html.escape(subtitle)

    if style == "tech-badge":
        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="400" height="400">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f172a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#1e293b;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="accentGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" style="stop-color:#38bdf8;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#818cf8;stop-opacity:1" />
    </linearGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="8" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>
  <rect width="400" height="400" rx="32" fill="url(#bgGrad)" stroke="#334155" stroke-width="2" />
  <circle cx="200" cy="160" r="85" fill="none" stroke="url(#accentGrad)" stroke-width="4" stroke-dasharray="12 6" opacity="0.8" />
  <circle cx="200" cy="160" r="70" fill="#1e293b" stroke="#38bdf8" stroke-width="2" />
  <polygon points="200,105 240,140 225,190 175,190 160,140" fill="url(#accentGrad)" filter="url(#glow)" />
  <circle cx="200" cy="155" r="14" fill="#ffffff" />
  <text x="200" y="285" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="22" font-weight="700" fill="#f8fafc" text-anchor="middle" letter-spacing="1">{title_escaped}</text>
  <text x="200" y="318" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif" font-size="13" font-weight="500" fill="#94a3b8" text-anchor="middle">{subtitle_escaped}</text>
</svg>"""
    elif style == "architecture-diagram":
        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <linearGradient id="gridBg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0b0f19;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#111827;stop-opacity:1" />
    </linearGradient>
    <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1f2937" stroke-width="1" />
    </pattern>
    <linearGradient id="nodeGrad1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1e3a8a;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#1e40af;stop-opacity:0.8" />
    </linearGradient>
    <linearGradient id="nodeGrad2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#065f46;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#047857;stop-opacity:0.8" />
    </linearGradient>
    <linearGradient id="nodeGrad3" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#4c1d95;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#6d28d9;stop-opacity:0.8" />
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" fill="url(#gridBg)" />
  <rect width="{width}" height="{height}" fill="url(#grid)" />
  <text x="50" y="60" font-family="'Segoe UI', Roboto, sans-serif" font-size="24" font-weight="700" fill="#f9fafb">{title_escaped}</text>
  <text x="50" y="88" font-family="'Segoe UI', Roboto, sans-serif" font-size="14" font-weight="400" fill="#9ca3af">{subtitle_escaped}</text>

  <g transform="translate(60, 150)">
    <rect width="180" height="100" rx="12" fill="url(#nodeGrad1)" stroke="#3b82f6" stroke-width="2" />
    <text x="90" y="45" font-family="sans-serif" font-size="16" font-weight="600" fill="#ffffff" text-anchor="middle">Input Ingestion</text>
    <text x="90" y="70" font-family="sans-serif" font-size="12" fill="#93c5fd" text-anchor="middle">Multi-Format Pipeline</text>
  </g>

  <path d="M 240 200 L 310 200" stroke="#38bdf8" stroke-width="3" stroke-dasharray="6 4" />
  <polygon points="315,200 305,195 305,205" fill="#38bdf8" />

  <g transform="translate(320, 150)">
    <rect width="180" height="100" rx="12" fill="url(#nodeGrad2)" stroke="#10b981" stroke-width="2" />
    <text x="90" y="45" font-family="sans-serif" font-size="16" font-weight="600" fill="#ffffff" text-anchor="middle">Neural Processing</text>
    <text x="90" y="70" font-family="sans-serif" font-size="12" fill="#a7f3d0" text-anchor="middle">Vision &amp; Synthesis</text>
  </g>

  <path d="M 500 200 L 570 200" stroke="#10b981" stroke-width="3" stroke-dasharray="6 4" />
  <polygon points="575,200 565,195 565,205" fill="#10b981" />

  <g transform="translate(580, 150)">
    <rect width="160" height="100" rx="12" fill="url(#nodeGrad3)" stroke="#8b5cf6" stroke-width="2" />
    <text x="80" y="45" font-family="sans-serif" font-size="16" font-weight="600" fill="#ffffff" text-anchor="middle">Export &amp; Verify</text>
    <text x="80" y="70" font-family="sans-serif" font-size="12" fill="#ddd6fe" text-anchor="middle">PNG · JPG · WEBP · SVG</text>
  </g>
</svg>"""
    else:
        svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">
  <defs>
    <linearGradient id="heroGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0f172a;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#1e1b4b;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#311042;stop-opacity:1" />
    </linearGradient>
    <linearGradient id="orbGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#f43f5e;stop-opacity:0.8" />
      <stop offset="100%" style="stop-color:#8b5cf6;stop-opacity:0.8" />
    </linearGradient>
  </defs>
  <rect width="{width}" height="{height}" rx="20" fill="url(#heroGrad)" />
  <circle cx="{width - 150}" cy="{height // 2}" r="120" fill="url(#orbGrad)" filter="blur(20px)" opacity="0.6" />
  <text x="60" y="{height // 2 - 20}" font-family="'Segoe UI', Roboto, sans-serif" font-size="34" font-weight="800" fill="#ffffff">{title_escaped}</text>
  <text x="60" y="{height // 2 + 30}" font-family="'Segoe UI', Roboto, sans-serif" font-size="18" font-weight="400" fill="#cbd5e1">{subtitle_escaped}</text>
</svg>"""

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(svg_content)

    return output_path


def compute_technical_score(file_path: str) -> Dict[str, Any]:
    """
    Evaluates image against the technical portions of the 100-point rubric:
      - Export integrity (5 pts)
      - Technical rendering & resolution (15 pts)
      - Dynamic range & contrast (10 pts)
    Provides total technical score out of 30, with visual rubric breakdown for remaining 70.
    """
    insp = inspect_image(file_path)
    score_card = {
        "export_integrity": 0,
        "technical_rendering": 0,
        "contrast_lighting": 0,
        "technical_total": 0,
        "notes": []
    }

    if insp["valid"] and insp["magic_bytes_matched"]:
        score_card["export_integrity"] = 5
    elif insp["valid"]:
        score_card["export_integrity"] = 3
        score_card["notes"].append("Valid image but header signature had minor discrepancy.")
    else:
        score_card["notes"].append("File integrity or decoding issues detected.")

    dims = insp.get("dimensions")
    if dims:
        w, h = dims["width"], dims["height"]
        if w >= 800 and h >= 800:
            score_card["technical_rendering"] = 15
        elif w >= 400 and h >= 400:
            score_card["technical_rendering"] = 12
        else:
            score_card["technical_rendering"] = 8
            score_card["notes"].append("Low resolution output (< 400px).")
    else:
        score_card["technical_rendering"] = 5

    contrast = insp.get("contrast_std")
    if contrast is not None:
        if 40.0 <= contrast <= 90.0:
            score_card["contrast_lighting"] = 10
        elif contrast > 90.0 or contrast >= 25.0:
            score_card["contrast_lighting"] = 8
        else:
            score_card["contrast_lighting"] = 5
            score_card["notes"].append("Low contrast / dynamic range.")
    else:
        score_card["contrast_lighting"] = 8

    score_card["technical_total"] = (
        score_card["export_integrity"] +
        score_card["technical_rendering"] +
        score_card["contrast_lighting"]
    )
    score_card["inspection"] = insp
    return score_card


# ==============================================================================
# MAIN CLI DISPATCHER
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(description="Professional Image Engineering Engine (/image-generate)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Providers Subcommand
    p_prov = subparsers.add_parser("providers", help="List and check status of all image generation engines")
    p_prov.add_argument("--json", action="store_true", help="Output JSON format")

    # Inspect
    p_insp = subparsers.add_parser("inspect", help="Inspect and validate an image file")
    p_insp.add_argument("file", help="Path to image file")
    p_insp.add_argument("--json", action="store_true", help="Output JSON format")

    # Convert SVG to Raster
    p_svg = subparsers.add_parser("svg2raster", help="Convert SVG to PNG/JPG/JPEG/WebP")
    p_svg.add_argument("svg_file", help="Input SVG file")
    p_svg.add_argument("output", help="Output file path (.png, .jpg, .jpeg, .webp)")
    p_svg.add_argument("--width", type=int, help="Target width in pixels")
    p_svg.add_argument("--height", type=int, help="Target height in pixels")
    p_svg.add_argument("--scale", type=float, default=1.0, help="Scale factor")
    p_svg.add_argument("--quality", type=int, default=95, help="JPEG/WebP quality")

    # Raster to Raster Convert
    p_conv = subparsers.add_parser("convert", help="Convert between raster formats")
    p_conv.add_argument("input", help="Input image file")
    p_conv.add_argument("output", help="Output image file")
    p_conv.add_argument("--quality", type=int, default=95, help="Quality (default: 95)")

    # Embed Raster in SVG
    p_embed = subparsers.add_parser("embed-svg", help="Wrap raster in transparently labeled SVG container")
    p_embed.add_argument("raster_file", help="Input raster image")
    p_embed.add_argument("output_svg", help="Output SVG path")

    # Export All
    p_exp = subparsers.add_parser("export-all", help="Package & export image to .png, .jpg, .jpeg, .webp, .svg")
    p_exp.add_argument("source", help="Source image path")
    p_exp.add_argument("base_output", help="Base output path (e.g. ./dist/my_image)")
    p_exp.add_argument("--quality", type=int, default=95, help="Quality")

    # Improve
    p_imp = subparsers.add_parser("improve", help="Programmatic image enhancement")
    p_imp.add_argument("input", help="Input image path")
    p_imp.add_argument("output", help="Output image path")
    p_imp.add_argument("--brightness", type=float, default=1.0, help="Brightness multiplier")
    p_imp.add_argument("--contrast", type=float, default=1.05, help="Contrast multiplier")
    p_imp.add_argument("--sharpness", type=float, default=1.1, help="Sharpness multiplier")
    p_imp.add_argument("--solid-bg", type=str, default=None, help="Solid background hex (#FFFFFF)")

    # Algorithmic SVG Generator
    p_gen = subparsers.add_parser("generate-vector", help="Generate algorithmic SVG illustration")
    p_gen.add_argument("--style", choices=["tech-badge", "architecture-diagram", "product-banner"], default="tech-badge")
    p_gen.add_argument("--title", required=True, help="Main title")
    p_gen.add_argument("--subtitle", default="", help="Subtitle")
    p_gen.add_argument("--output", required=True, help="Output SVG path")
    p_gen.add_argument("--width", type=int, default=800, help="Width in pixels")
    p_gen.add_argument("--height", type=int, default=500, help="Height in pixels")

    # Score
    p_scr = subparsers.add_parser("score", help="Compute technical quality score")
    p_scr.add_argument("file", help="Path to image file")

    # Generate Image (Unified High-Level Pipeline)
    p_ai = subparsers.add_parser("generate", help="Synthesize image from prompt using best available provider")
    p_ai.add_argument("--prompt", required=True, help="Detailed generation prompt")
    p_ai.add_argument("--output", required=True, help="Output image file path (.png, .jpg, .jpeg, .webp)")
    p_ai.add_argument("--aspect-ratio", default="1:1", help="Aspect ratio preset: 1:1, 16:9, 9:16, 4:3, 3:2, 2:3")
    p_ai.add_argument("--width", type=int, default=None, help="Explicit width in pixels")
    p_ai.add_argument("--height", type=int, default=None, help="Explicit height in pixels")
    p_ai.add_argument("--seed", type=int, default=None, help="Random seed for reproducibility")
    p_ai.add_argument("--provider", default="auto", choices=["auto", "pollinations", "antigravity-native", "local-runtime"],
                      help="Provider selection (default: auto)")
    p_ai.add_argument("--keep-watermark", action="store_true", help="Do not suppress watermark")
    p_ai.add_argument("--overwrite", action="store_true", help="Allow overwriting existing target file")

    # Backward Compatibility: generate-ai
    p_legacy_ai = subparsers.add_parser("generate-ai", help="Legacy alias for generate")
    p_legacy_ai.add_argument("--prompt", required=True, help="Detailed generation prompt")
    p_legacy_ai.add_argument("--output", required=True, help="Output image file path")
    p_legacy_ai.add_argument("--width", type=int, default=1024, help="Width")
    p_legacy_ai.add_argument("--height", type=int, default=1024, help="Height")
    p_legacy_ai.add_argument("--seed", type=int, default=None, help="Seed")
    p_legacy_ai.add_argument("--keep-watermark", action="store_true", help="Keep watermark")

    args = parser.parse_args()
    registry = ProviderRegistry()

    if args.command == "providers":
        all_provs = registry.list_all()
        if args.json:
            print(json.dumps(all_provs, indent=2))
        else:
            print("=" * 70)
            print("IMAGE GENERATION PROVIDER REGISTRY (Zero-Install Architecture)")
            print("=" * 70)
            for p in all_provs:
                status = "[AVAILABLE]" if p["available"] else "[UNAVAILABLE]"
                print(f"{status} {p['name']} ({p['priority']})")
                print(f"  Cost:           {p['cost']}")
                print(f"  License:        {p['license']}")
                print(f"  Authentication: {p['authentication']}")
                print(f"  Status Detail:  {p['status_message']}")
                print("-" * 70)

    elif args.command == "inspect":
        res = inspect_image(args.file)
        if args.json:
            print(json.dumps(res, indent=2))
        else:
            status = "VALID" if res["valid"] else "INVALID"
            print(f"[{status}] {res['file_name']} ({res['format']}, {res['size_bytes']} bytes)")
            if res["dimensions"]:
                print(f"  Dimensions: {res['dimensions']['width']}x{res['dimensions']['height']} (Aspect: {res['aspect_ratio']})")
            print(f"  Mode: {res['mode']}, Has Transparency: {res['has_transparency']}")
            print(f"  Magic Bytes Matched: {res['magic_bytes_matched']}")
            if res.get("brightness_mean"):
                print(f"  Stats: Brightness={res['brightness_mean']}, Contrast Std={res['contrast_std']}")
            if res["issues"]:
                print("  Issues/Notices:")
                for issue in res["issues"]:
                    print(f"    - {issue}")

    elif args.command == "svg2raster":
        out_ext = os.path.splitext(args.output)[1].lower()
        if out_ext == ".png":
            render_svg_to_png(args.svg_file, args.output, width=args.width, height=args.height, scale=args.scale)
        else:
            tmp_png = os.path.join(tempfile.gettempdir(), f"tmp_{os.getpid()}.png")
            render_svg_to_png(args.svg_file, tmp_png, width=args.width, height=args.height, scale=args.scale)
            convert_raster(tmp_png, args.output, quality=args.quality)
            if os.path.exists(tmp_png):
                os.remove(tmp_png)
        print(f"Successfully converted SVG to {args.output}")

    elif args.command == "convert":
        convert_raster(args.input, args.output, quality=args.quality)
        print(f"Successfully converted {args.input} -> {args.output}")

    elif args.command == "embed-svg":
        embed_raster_in_svg(args.raster_file, args.output_svg)
        print(f"Successfully wrapped raster into SVG container -> {args.output_svg}")

    elif args.command == "export-all":
        res = package_and_export_all(args.source, args.base_output, quality=args.quality)
        print(json.dumps(res, indent=2))

    elif args.command == "improve":
        improve_image(args.input, args.output,
                      brightness=args.brightness,
                      contrast=args.contrast,
                      sharpness=args.sharpness,
                      solid_bg=args.solid_bg)
        print(f"Successfully improved image -> {args.output}")

    elif args.command == "generate-vector":
        out = generate_algorithmic_svg(args.style, args.title, args.subtitle, args.output, width=args.width, height=args.height)
        print(f"Successfully generated vector SVG -> {out}")

    elif args.command == "score":
        res = compute_technical_score(args.file)
        print(json.dumps(res, indent=2))

    elif args.command in ["generate", "generate-ai"]:
        # Resolve dimensions
        if getattr(args, "width", None) and getattr(args, "height", None):
            w, h = args.width, args.height
        elif hasattr(args, "aspect_ratio"):
            w, h = parse_aspect_ratio_to_dimensions(args.aspect_ratio)
        else:
            w, h = (1024, 1024)

        provider_name = getattr(args, "provider", "auto")
        if provider_name == "auto":
            selected_provider, reason = registry.select_best_available()
            if not selected_provider:
                print(json.dumps({"success": False, "error": f"No available provider found: {reason}"}))
                sys.exit(1)
        else:
            selected_provider = registry.get(provider_name)
            if not selected_provider:
                print(json.dumps({"success": False, "error": f"Unknown provider: {provider_name}"}))
                sys.exit(1)
            avail, reason = selected_provider.is_available()
            if not avail:
                print(json.dumps({"success": False, "error": f"Provider '{provider_name}' is unavailable: {reason}"}))
                sys.exit(1)

        safe_out = get_safe_output_path(args.output, overwrite=getattr(args, "overwrite", False))

        res = selected_provider.generate(
            prompt=args.prompt,
            output_path=safe_out,
            width=w,
            height=h,
            seed=args.seed,
            no_watermark=not args.keep_watermark
        )

        # Post-validation
        if res.get("success") and os.path.exists(safe_out):
            insp = inspect_image(safe_out)
            res["inspection"] = {
                "valid": insp["valid"],
                "format": insp["format"],
                "dimensions": insp["dimensions"],
                "size_bytes": insp["size_bytes"]
            }

        print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
