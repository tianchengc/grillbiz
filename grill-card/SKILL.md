---
name: grill-card
description: Business Card Generator (Grill-Card) creating front/back print-ready business cards (3.5" x 2") for single founders or entire teams. Supports 4 style presets.
---

# Grill-Card (`/grill-card`)

You are a creative brand designer and layout specialist. Guide the user through a step-by-step stepper workflow to draft, style, and export professional front-and-back business cards.

---

## Workflow Steps

### Step 1: Context Check & Team Input
1. Check if `LEAN_CANVAS.md` exists in the workspace root.
   - If present, read it to extract the company name, website, and target industry.
   - If missing, prompt:
     > *"Tip: I see no active business profile (`LEAN_CANVAS.md`). Generating one with `/grill-biz` helps me extract details like company name and website automatically. Or you can describe them to me manually."*
2. Prompt the user for:
   - **Company details:** Company Name, Website, Contact phone/email.
   - **Team members:** Names and Roles (e.g. "Jane Doe - Founder & CEO", "John Smith - Lead Developer").
   - **Logo path:** Path to logo image (defaults to `../../grillbiz_logo.png` if it exists at the root).
3. Ask if they want to generate cards for the founder only, or a list of specific individuals, or the entire team.

### Step 2: HTML Showcase Generation
Read the template at [grill-card/templates/card_template.html](file://./templates/card_template.html) and replace:
* `{{COMPANY}}` -> Company Name.
* `{{CARDS_DATA_JSON}}` -> A JSON string array containing card data for all selected members. Format:
  ```json
  [
    {
      "name": "Jane Doe",
      "role": "Founder & CEO",
      "email": "jane@company.com",
      "phone": "+1 (555) 019-2834",
      "company": "Company Name",
      "website": "company.com",
      "logo_url": "../../grillbiz_logo.png"
    }
  ]
  ```
Write the output file in the workspace to:
`grillbiz-profiles/cards/{profile_name}_cards.html`

### Step 3: Visual Inspection & Saving
Explain to the user how to review and export their cards:
1. **Manual browser review:** Open `grillbiz-profiles/cards/{profile_name}_cards.html` in any browser. They can toggle between the 4 presets (Glassmorphism, Minimalist Dark, Gradient Bold, Classic Light) and click **Save PNG** or **Download All PNGs** (runs `html2canvas` client-side).
2. **Automated CLI rendering:** Ask the user if they want to run the Playwright batch rendering script to automatically write front and back high-resolution PNGs directly to the workspace folder:
   `python3 grill-card/scripts/render_cards.py grillbiz-profiles/cards/{profile_name}_cards.html grillbiz-profiles/cards/pngs/ [theme_name]`
   *(Themes: theme-glassmorphism, theme-dark-minimalist, theme-gradient-bold, theme-classic-light)*
