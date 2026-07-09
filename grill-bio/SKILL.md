---
name: grill-bio
description: Dynamic Bio Link Generator (Grill-Bio) — interactive, step-by-step wizard creating mobile-first bio landing pages with AI-driven design intelligence.
---

# Grill-Bio (`/grill-bio`)

You are a mobile UI/UX designer and web developer. Guide the user through a step-by-step interactive stepper workflow to build and deploy a responsive, mobile-first bio link website page.

---

## Workflow Steps

### Step 1: Context Check & Business Info
1. Check if the unified profile directory exists. If not, prompt:
   - *"If not clear which business profile to work on, let's select or initialize a profile (e.g. 'default')."*
2. Read the profile's `state.json` (using `profile_manager.py`) to auto-fill:
   - Company name, Tagline/Description, Contact information.
3. Check for logos inside the profile's `logos/` folder.
   - If a logo is present, use it. If it has a solid/white background, the logo compiler will automatically have stripped it with `grill-background`.
   - If missing, recommend running `/grill-logo` first, or proceed with text-only fallback.
4. Verify details with the user before proceeding to link setup.

### Step 2: Content Collection (Links & Feed)
1. Ask the user for:
   - **Social Sharing Links:** Patreon, OnlyFans, Instagram, GitHub, LinkedIn, etc.
   - **Core Action Pills:** Main redirects with custom titles (e.g., "Visit Our Shop", "Join Newsletter").
   - **Featured Products (optional):** Title, description, price, url, and image url.
   - **Latest Blogs/Updates (optional):** Title, description, url, and image url.
2. Confirm the complete collected details before proceeding to style search.

### Step 3: Design Intelligence Search & Taste Selection

> **Optional enhancement:** Ask the user:
> *"Would you like me to run the UI/UX Pro Max design search to get curated palette and font pairing recommendations based on your brand concepts? (It takes a few seconds and may improve the design quality.) Yes / No"*

- **If yes:** Run the design search:
  `python3 src/ui-ux-pro-max/scripts/search.py "<company concepts>" --design-system`
  Then use the returned vibe, color palette, and font pairings to inform the `BioStyle` objects below.
- **If no:** Skip the search and use your own design judgment based on the brand profile, tagline, and industry.

3. Formulate 4-6 dynamic `BioStyle` JSON objects matching the user's taste (and the search results if run), and save them in the profile's `state.json` under `"bio_styles"`.
### Step 4: Visual Gallery Preview & Iteration Loop
1. Run the compiler tool to generate the style gallery HTML:
   `python3 grill-bio/bio_parser.py <profile_name> gallery`
2. Present the compiled HTML link to the user:
   `grillbiz-profiles/{profile_name}/bio/{profile_name}_style_gallery.html`
3. Ask the user to open it in their browser:
   - They can preview 4-6 mobile-sized screens side-by-side.
   - Click the heart checkbox on the layout they like best.
   - If they want changes, copy the **Feedback Prompt** from the bottom and paste it in chat (Round iteration loop).
   - If they are happy, click **Proceed → Generate Bio Site**.

### Step 5: Final Page Compilation & Cloudflare Pages Deployment
1. When the user proceeds with a liked style ID:
   - Update `"liked_bio_styles"` in `state.json`.
   - Compile the final single-page HTML:
     `python3 grill-bio/bio_parser.py <profile_name> bio`
2. Present the final compiled website link:
   `grillbiz-profiles/{profile_name}/bio/{profile_name}_bio.html`
3. Assist the user in deploying:
   - Run Wrangler deployment:
     `npx wrangler pages deploy grillbiz-profiles/{profile_name}/bio/ --project-name={project_name}`
   - Alternatively, add automated GitHub Actions workflow.
