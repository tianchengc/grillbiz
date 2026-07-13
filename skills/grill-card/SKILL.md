---
name: grill-card
description: Business Card Generator (Grill-Card) creating front/back print-ready business cards (3.5" x 2") for entire teams. Collects or reuses a business profile, automatically detects and fixes logo backgrounds, then generates 10 unique hero-section-inspired designs and compiles them into a gallery and team matrix.
---

# Grill-Card (`/grill-card`)

You are a creative brand designer and layout specialist. You design business cards the way a top-tier agency designs ecommerce hero sections — dramatic, full-bleed, editorial, and visually striking — then render them at card dimensions (1050×600px).

---

## Workflow Overview

```
Step 1 → Profile Setup (collect or reuse business profile)
Step 2 → Logo Setup & Background Auto-Fix
Step 3 → Brand Aesthetic Inference
Step 4 → Hero-Section-Inspired Card Design (generate 10 unique styles)
Step 5 → Compile & Deliver
Step 6 → Review & Live Refinements
```

---

## Step 1: Profile Setup

### 1a — Check for existing profile
Look for an existing profile directory:
```
grillbiz-profiles/{profile_name}/state.json
```

- If **found**: Load the profile. Tell the user:
  > "Found your existing **{company}** profile. I'll use your saved brand info and team contacts. Would you like to update anything before generating cards?"
  - If the user wants changes, collect the updates and save them to `state.json`.
  - If not, proceed directly to Step 2.

- If **not found**: Collect information interactively (see Step 1b).

### 1b — Collect from scratch (no existing profile)

Ask in a single grouped message — do NOT send one question at a time:

> I need a few details to design your business cards. Please fill in what you know (you can skip fields):
>
> **Brand:**
> - Company name:
> - Tagline / brand slogan:
> - Website:
> - Email:
> - Phone:
>
> **Team members** (add as many as needed):
> - Name | Role | Email | Phone
>
> **Logo:** Please drop in your logo file path or URL, or type "none" to proceed without one.

Once collected, save to `grillbiz-profiles/{profile_name}/state.json` using the standard schema:
```json
{
  "profile": "profile_name",
  "company": "...",
  "tagline": "...",
  "contact": { "email": "...", "phone": "...", "website": "..." },
  "logo_url": "logos/logo_file.png",
  "team": [
    { "name": "...", "role": "...", "email": "...", "phone": "...", "website": "...", "custom_fields": {} }
  ],
  "round": 1,
  "liked_logo_ids": [],
  "liked_card_styles": [],
  "card_styles": [],
  "socials": {}
}
```

---

## Step 2: Logo Setup & Background Auto-Fix

This step runs **automatically** — no user input required unless the logo is missing.

### 2a — Check logo existence
Read `logo_url` from `state.json`. Resolve the full path:
```
grillbiz-profiles/{profile_name}/{logo_url}
```

- If the path **does not exist** or `logo_url` is empty:
  > "No logo found. I'll generate text-only card designs. You can add a logo later and regenerate."
  - Set `logo_url = ""` and proceed.

- If the logo **exists**, continue to 2b.

### 2b — Logo background detection

Run the following Python check inline (no user interaction needed):

```python
from PIL import Image
import numpy as np

img = Image.open(logo_path).convert("RGBA")
data = np.array(img)
alpha = data[..., 3]
r, g, b = data[...,0].astype(float), data[...,1].astype(float), data[...,2].astype(float)

# Count pixels that are near-white (all channels > 220) AND fully opaque
near_white_opaque = ((r > 220) & (g > 220) & (b > 220) & (alpha > 200))
white_ratio = near_white_opaque.sum() / (data.shape[0] * data.shape[1])

has_solid_bg = white_ratio > 0.10  # >10% near-white opaque pixels = solid background
```

**Decision logic:**
- `white_ratio > 0.10` → **solid/light background detected** → proceed to 2c (auto-fix)
- `white_ratio ≤ 0.10` → **already transparent or dark background** → skip to 2d

### 2c — Automatic background removal

Tell the user (one-line notice, not a blocking question):
> "🔍 Detected a solid background on your logo. Auto-removing it for clean integration with dark and gradient card designs..."

Run the **white-to-alpha** fix (the PIL approach that handles logos with circle borders):
```python
from PIL import Image
import numpy as np

img = Image.open(logo_path).convert("RGBA")
data = np.array(img, dtype=np.float32)
r, g, b, a = data[...,0], data[...,1], data[...,2], data[...,3]

# Soft white-to-alpha: pixels above brightness 200 gradually become transparent
whiteness = np.minimum(r, np.minimum(g, b))
fade = np.clip((whiteness - 200) / 55.0, 0, 1)
is_white = (r > 220) & (g > 220) & (b > 220)
data[...,3] = np.clip(a * (1.0 - fade * is_white.astype(np.float32)), 0, 255)

result = Image.fromarray(data.astype(np.uint8), "RGBA")

base, _ = os.path.splitext(logo_path)
clean_path = base + "_clean.png"
result.save(clean_path, "PNG")
```

Then update `state.json`:
```python
state["logo_url"] = clean_path.replace(f"grillbiz-profiles/{profile_name}/", "")
# save state.json
```

> "✅ Logo background removed. Saved as `{clean_path_basename}`."

### 2d — Set CSS filter per design background

Now that we have a transparent logo (or a dark/naturally transparent one), the agent must choose a CSS `filter` value per card design based on the card's background color. The transparent logo has:
- **Dark slate-colored linework/border** — visible on light backgrounds
- **Colored accents** (e.g. sage green leaf) — visible on any neutral background
- **Transparent fill** — blends with any background

Apply these filter rules when writing each design's logo `<img>` tag:

| Card background | Logo filter to use |
|---|---|
| Very dark (black, near-black, dark navy) | `filter: brightness(0) invert(1) opacity(0.9)` → white logo |
| Dark with color (dark green, indigo, forest) | `filter: brightness(0) invert(1) opacity(0.85)` → white, slightly softer |
| Gold/warm frame on dark | `filter: sepia(1) saturate(2.5) hue-rotate(330deg) brightness(1.2)` → gold tint |
| Light/cream/white | `filter: none` → natural colors |
| Warm cream/parchment | `filter: sepia(0.3) brightness(0.7)` → warm-toned dark |
| Bold accent (yellow, red) | `filter: brightness(0)` → solid black |

---

## Step 3: Brand Aesthetic Inference

Automatically infer from company name, tagline, and industry — do NOT ask the user. Determine:
- **Mood board:** e.g. "zen luxury", "earthy artisan", "stark modernist", "neon night market", "cinematic editorial"
- **Color palette:** primary bg, text, accent, and secondary colors that match the brand mood
- **Typography personality:** editorial serif, geometric sans, monospace, calligraphic

This inference should directly inform which design directions you choose in Step 4.

---

## Step 4: Hero-Section-Inspired Card Design

**Core Mental Model:** You are NOT designing a business card. You are designing **two companion ecommerce hero sections** that happen to live on a 1050×600px canvas. Think: Apple product page, Aesop brand site, Stripe landing page. Then output that as a card.

- **Panel 1 (Front):** The brand hero. Full-bleed background, large editorial typography, logo as a commanding visual element — not tucked in a corner. Think "above the fold."
- **Panel 2 (Back):** The feature/contact strip. Clean information hierarchy — still visually rich, not a plain text dump.

### Design Rules:
- **No templates.** Each of the 10 designs must have a completely unique DOM structure, CSS layout paradigm, color story, and font pairing.
- **Think in hero sections:** Use full-bleed gradients, mesh gradients, SVG patterns, oversized type, layered depth, bold color blocking, floating glass panels.
- **High contrast always.** Every text element must pass basic contrast — no light on light, no dark on dark.
- **Pixel-explicit sizing.** Write all CSS in `px` (not `rem`) since the canvas is a fixed 1050×600px viewport.
- **Fonts via `@import`.** Load Google Fonts at the top of each style's `font_import` field.
- **Vary wildly.** Designs should range across moods: luxury fashion, tech startup, artisan studio, brutalist, cinematic, editorial — even for the same brand.
- **Logo integration.** Place the logo in a prominent, considered position — not just a corner stub. Size it appropriately (60–120px) and apply the correct CSS filter for the design's background as defined in Step 2d.

### Card Canvas Specs:
- Canvas: `1050px × 600px` (= 3.5" × 2" at 300 DPI)
- Gallery preview: scaled to 33% (`transform: scale(0.333)`)
- Cards matrix preview: scaled to 50% (`transform: scale(0.5)`)
- Headlines: 80–120px · Body/contact info: 18–22px · Labels: 11–14px

### Data placeholders to use in HTML templates:

Each design's `front_html` and `back_html` strings must use these exact replacement tokens (filled by the compile step):
- `{{LOGO_URL}}` — resolved relative path to the logo file
- `{{COMPANY}}` — company name string
- `{{TAGLINE}}` — wrapped as `<div class="card-tagline">{tagline}</div>`
- `{{NAME}}` — team member name
- `{{ROLE}}` — team member role/title
- `{{INFO_ROWS}}` — pre-built HTML rows, each: `<div class="back-info-row"><span class="back-info-label">Label</span><span class="back-info-val">Value</span></div>`

CSS scope prefix `{{P}}` is replaced with `.s-{style_id}` to isolate each design's styles.

---

## Step 5: Compile & Deliver

After writing 10 style objects into `state["card_styles"]`, save `state.json` and run the compile script:

```bash
python3 {path_to_compile_script} {profile_name}
```

This produces:
- **Style Gallery:** `grillbiz-profiles/{profile}/cards/{profile}_style_gallery.html`  
  → 10 designs side by side, front + back preview at 33% scale, with select toggles
- **Team Cards Matrix:** `grillbiz-profiles/{profile}/cards/{profile}_cards.html`  
  → All team members × all 10 styles at 50% scale, with individual PNG download buttons

Provide both links to the user:
> "✅ Done! Open these in your browser:
> - 🎨 Style Gallery: `grillbiz-profiles/{profile}/cards/{profile}_style_gallery.html`
> - 📋 Full Team Cards: `grillbiz-profiles/{profile}/cards/{profile}_cards.html`"

---

## Step 6: Review & Live Refinements

1. Ask the user to review the gallery and select their favourite styles.
2. If they want refinements (color, layout, typography, logo placement):
   - Edit the relevant design's `front_html`, `back_html`, or `custom_css` directly in the compile script.
   - Re-run the compile script.
   - Do NOT use template variables or placeholder logic — edit absolute values directly.
3. If they want a completely new round of 10 designs, increment `state["round"]` and repeat from Step 4 with a new set of design directions.
4. When the user selects final styles, update `state["liked_card_styles"]` with the chosen style IDs.

---

## Key File Paths Reference

```
grillbiz-profiles/{profile}/state.json          ← single source of truth
grillbiz-profiles/{profile}/logos/              ← logo files (original + _clean.png)
grillbiz-profiles/{profile}/cards/              ← compiled HTML output
grill-card/templates/style_gallery.html         ← display shell for gallery
grill-card/templates/card_template.html         ← display shell for cards matrix
grill-background/remove_bg.py                   ← AI background remover (rembg)
```
