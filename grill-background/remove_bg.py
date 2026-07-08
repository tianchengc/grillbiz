#!/usr/bin/env python3
"""
Grill-Background: AI-powered background remover using rembg.
Usage:
    python3 grill-background/remove_bg.py <input_path> [output_path]

If output_path is omitted, saves to same directory with _nobg.png suffix.
Auto-installs rembg if not present.
"""

import sys
import os
import subprocess


def ensure_rembg():
    """Install rembg and its onnxruntime dependency if not already available."""
    # Step 1: ensure onnxruntime (rembg[cli] doesn't always pull it on Python 3.9)
    try:
        import onnxruntime  # noqa: F401
    except ImportError:
        print("📦 onnxruntime not found. Installing…")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "onnxruntime", "--quiet"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print("❌ Failed to install onnxruntime.")
            print(result.stderr)
            sys.exit(1)
        print("✅ onnxruntime installed.")

    # Step 2: ensure rembg itself
    try:
        import rembg  # noqa: F401
        return True
    except ImportError:
        print("📦 rembg not found. Installing (this may take a moment on first run)…")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "rembg[cli]", "--quiet"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print("❌ Failed to install rembg. Please run manually:")
            print("   pip install rembg[cli]")
            print(result.stderr)
            sys.exit(1)
        print("✅ rembg installed successfully.")
        return True


def remove_background(input_path: str, output_path: str = None) -> str:
    """Remove the background from an image file."""
    ensure_rembg()

    from rembg import remove
    from PIL import Image
    import io

    if not os.path.exists(input_path):
        print(f"❌ Input file not found: {input_path}")
        sys.exit(1)

    # Build output path
    if not output_path:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}_nobg.png"

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    print(f"🔍 Processing: {input_path}")
    print(f"💾 Output:     {output_path}")

    with open(input_path, "rb") as f:
        input_data = f.read()

    # Run background removal
    output_data = remove(input_data)

    # Save as RGBA PNG
    img = Image.open(io.BytesIO(output_data)).convert("RGBA")
    img.save(output_path, "PNG")

    size_kb = os.path.getsize(output_path) // 1024
    print(f"✅ Background removed! Saved to: {output_path} ({size_kb} KB)")
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 grill-background/remove_bg.py <input_path> [output_path]")
        print("")
        print("Examples:")
        print("  python3 grill-background/remove_bg.py grillbiz-profiles/logos/default/logo_1_1.png")
        print("  python3 grill-background/remove_bg.py my_logo.jpg my_logo_transparent.png")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    remove_background(input_path, output_path)
