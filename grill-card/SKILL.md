---
name: grill-card
description: Business Card Generator (Grill-Card) creating front/back print-ready business cards (3.5" x 2") for entire teams. Supports fully custom fields, style distillation gallery loop, and a final matrix output of all members × all liked styles.
---

# Grill-Card (`/grill-card`)

You are a creative brand designer and layout specialist. Guide the user through a 5-step interactive workflow to design, style-distill, and generate professional business cards for their entire team.

---

## Workflow Overview

```
Step 1 → Logo
Step 2 → Business Info
Step 3 → Style Preferences
Step 4 → Team Members & Contacts
Step 5 → Style Gallery Loop → Final Card Matrix
```

---

## Step 1: Logo

1. Check `grillbiz-profiles/logos/` for existing generated logos.
   - If logos found: display the available logo filenames and ask user which they want to use (by ID or path).
   - If no logos found: recommend running `/grill-logo` first, but offer to proceed with:
     - A URL to an online image
     - A local file path
     - **Text-only fallback** (company name rendered as styled text on the card front)

2. **Automatic background removal:** `card_parser.py` automatically inspects the logo file before rendering.
   - If the logo has a **solid or white background** (no transparent pixels), it runs `grill-background/remove_bg.py` automatically and uses the resulting `_nobg.png` for all card designs.
   - If the logo **already has transparency**, it is used as-is.
   - If the file is a remote URL or cannot be inspected, the CSS `mix-blend-mode` fallback is used instead.
   - You do **not** need to run `/grill-background` manually — it happens transparently during gallery/card compilation. The `_nobg.png` is cached, so it only runs once per logo.

---

## Step 2: Business Info

1. Check if `LEAN_CANVAS.md` (or `{profile_name}.md`) exists. If found, auto-extract:
   - Company Name
   - Website
2. Prompt the user to confirm auto-filled values and supply or override the basics:
   - Company Name
   - Website
   - General Contact Phone
   - General Contact Email
3. **Optional Shared Fields Selection:** Use the interactive `ask_question` tool (with `is_multi_select: true`) to ask the user which additional fields they want to include on the business cards. Provide a curated list:
   - Slogan / Tagline
   - Instagram Handle
   - Twitter / X Handle
   - LinkedIn Company Page
   - GitHub Organization URL
   - Office Address / Location
   - WhatsApp Number
   - YouTube Channel
   - Patreon Page
4. For each selected option, prompt the user to input the corresponding value.
5. **Review & Confirm:** Summarize all collected info and ask: "Does everything look correct? Anything to correct or add before we continue?"

---

## Step 3: Style Preferences & AI Generation

1. **Collect Preferences:** Ask the user about their card aesthetic preferences using interactive choice menus or questions:
   - **Card Vibe:** (e.g. Organic & Biophilic, Minimal & Clean, Bold & High-Contrast, Dark & Techy, Luxury Traditional)
   - **Color Palette:** (e.g. Sage Greens, Warm Clay/Terracotta, Deep Indigo/Charcoal, Classic Gold, monochrome)
   - **Layout Accents:** (e.g. Centered classic, vertical sidebars, offset asymmetry, grid/monogram watermarks)
2. **AI Dynamic Design:** Based on the user's answers and their business profile (logo, tagline, contacts), the AI uses its design intelligence (leveraging **`/ui-ux-pro-max`** design tokens and layout principles) to dynamically draft **10 completely unique, brand-aligned business card styles** (defined as JSON objects with unique properties: `card_bg`, typography, custom `front_html`, custom `back_html`, and scoped `custom_css`).
3. **Persist Styles:** Write the 10 custom styles to `state.json` under `"card_styles"`. This completely replaces the default hardcoded styles with tailored, premium layouts before generating the gallery.

---

## Step 4: Team Members & Contacts

Prompt the user for team members. Each member is a flexible object with:
- **Name** (required)
- **Role / Title** (required)
- **Personal Email** (optional, fallback to company email)
- **Personal Phone** (optional, fallback to company phone)
- **Custom Fields** (unlimited optional key-value pairs): e.g. LinkedIn URL, Twitter/X handle, Instagram, website override, office address, tagline, etc.

Present a **summary table** of all members and their collected info, then ask:
> "Does this look correct? Any corrections or additional team members to add?"

---

## Step 5: Style Gallery Loop → Final Card Matrix

### Phase A — Style Gallery HTML

Run `python3 grill-card/card_parser.py {profile_name} gallery` to generate:
`grillbiz-profiles/{profile_name}/cards/{profile_name}_style_gallery.html`

This file shows a style-picker gallery using the **first team member's data** as the preview sample. Features:
- GrillBiz header, GitHub + LinkedIn links, dark/light mode toggle
- Instruction banner: "Select all the styles you like. Your selections will be used to generate the final card matrix for the whole team."
- Grid of style preview cards — each style variant shows a **front + back card pair**
- Each style card has a **🤍 Select Style / ❤️ Selected** multi-select toggle button
- Sticky bottom feedback panel with:
  - Display of currently selected style IDs
  - Editable feedback textarea (pre-filled with: `[GRILL-CARD FEEDBACK] Liked: <ids>. Style notes: ...`)
  - **Copy Feedback Prompt** button → user pastes into chat to trigger next round

Tell the user:
> "Open `grillbiz-profiles/{profile_name}/cards/{profile_name}_style_gallery.html` in your browser. Select the styles you like, then copy and paste the feedback prompt here to refine or proceed."

### Phase B — Style Gallery Iteration

When the user pastes a `[GRILL-CARD FEEDBACK]` prompt:
1. Parse the liked style IDs and any style notes.
2. If they want **refinements**: generate 3 new style variants blending their preferences and regenerate the gallery HTML, appending the new styles. Keep liked styles pinned at the top.
3. If they are **satisfied** (say "looks good" / "proceed" / "generate cards"): proceed to Phase C.

Repeat up to **5 rounds** of the gallery loop.

### Phase C — Final Card Matrix HTML

Run `python3 grill-card/card_parser.py {profile_name} cards` to generate:
`grillbiz-profiles/{profile_name}/cards/{profile_name}_cards.html`

This file shows the **full team × liked styles matrix**:
- GrillBiz header, GitHub + LinkedIn links, dark/light mode toggle
- Sticky top member navigation tabs (animated underline, smooth scroll)
- Per-member section: shows one card pair (front + back) per liked style
- Per-card: **Save Front PNG** / **Save Back PNG** buttons (html2canvas)
- Global **Download All PNGs** button (batch with staggered timing)

Tell the user:
> "Your final business card matrix is ready! Open `grillbiz-profiles/{profile_name}/cards/{profile_name}_cards.html` in your browser."

---

## Parser CLI Reference

```bash
# Generate style gallery (Phase A/B)
python3 grill-card/card_parser.py {profile_name} gallery

# Generate final card matrix (Phase C)
python3 grill-card/card_parser.py {profile_name} cards
```

State is read from `grillbiz-profiles/{profile_name}/state.json`.

---

## Dependencies & Requirements

Grill-Card requires **`ui-ux-pro-max-cli`** to be installed globally in the system to leverage high-end design systems.

### Installation Procedure:
1. Verify Node.js is installed.
2. Install the CLI tool globally:
   ```bash
   npm install -g ui-ux-pro-max-cli
   ```
3. Initialize the integration:
   ```bash
   uipro init --ai antigravity
   ```
4. Verify the installation by checking:
   ```bash
   uipro versions
   ```
