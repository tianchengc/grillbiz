---
name: grill-background
description: Background Remover (Grill-Background) — strips the background from any image using the rembg AI model. Outputs a transparent PNG suitable for use on any business card, logo, or design. Use when a logo or photo has a white or solid background that clashes with dark/gradient card themes.
---

# Grill-Background (`/grill-background`)

You are an image processing assistant. Remove the background from images so they can be used cleanly on any card or design surface.

---

## When to Use

- A logo image has a **white or solid-color background** that clashes with dark/gradient business card themes
- A photo needs a **transparent background** before being embedded in a design
- The user says "remove the background from my logo/image"

---

## Workflow

### Step 1: Identify the Image

Check if the user provided:
- A **local file path** to an image (PNG, JPG, WEBP)
- A **logo ID** from `grillbiz-profiles/logos/` (e.g. `logo_1_1`)

If a logo ID is provided, resolve the path:
```
grillbiz-profiles/logos/{profile}/logo_{id}.png
```

If no image is provided, ask:
> "Please provide the path or ID of the image you'd like to remove the background from."

### Step 2: Check & Install Dependencies

Run the background removal script which auto-installs `rembg` if missing:

```bash
python3 grill-background/remove_bg.py <input_path> [output_path]
```

- `input_path`: path to the original image
- `output_path` (optional): where to save the result. Defaults to same location with `_nobg.png` suffix.

**Example:**
```bash
python3 grill-background/remove_bg.py grillbiz-profiles/logos/default/logo_1_1.png
# → saves grillbiz-profiles/logos/default/logo_1_1_nobg.png
```

### Step 3: Update State

If the image was a logo being used in a card profile, offer to update `state.json` to point to the new transparent-background version:

> "Background removed! Saved to `logo_1_1_nobg.png`. Would you like me to update your card profile to use the new transparent logo?"

If yes, update `grillbiz-profiles/cards/{profile}/state.json`:
- Change `"logo_url"` to point to the `_nobg.png` file
- Recompile the card gallery and matrix:

```bash
python3 grill-card/card_parser.py {profile} gallery
python3 grill-card/card_parser.py {profile} cards
```

### Step 4: Confirm

Tell the user:
> "✅ Done! The logo now has a transparent background. Open the updated card gallery to see how it looks across all styles."

---

## Notes

- `rembg` uses the `u2net` AI model (~170MB, downloaded automatically on first run).
- Output is always a **32-bit RGBA PNG** with a transparent background.
- For logos, `mix-blend-mode` CSS in the card templates also helps blend non-transparent logos — but true transparency always looks better.
- Outputs go into `grillbiz-profiles/` which is gitignored, so the processed images are never committed.
