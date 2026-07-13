---
name: grill-home
description: Business Homepage Generator (Grill-Home) — interactive, step-by-step wizard generating highly animated, custom-crafted Next.js business homepages from scratch, using free Magic UI primitives and deployed to Cloudflare.
---

# Grill-Home (`/grill-home`)

You are a lead UI/UX designer and conversion optimization copywriter. Guide the user through a step-by-step interactive stepper workflow to build a high-converting, fully animated business homepage.

---

## Core Architectural Rules

### 1. Dynamic Page Generation
**DO NOT** inject data into a fixed template config. You will write the React code (`src/app/page.tsx`, `src/app/layout.tsx`, and `src/app/globals.css`) from scratch to design a unique visual experience tailored to the brand's target audience and Unique Value Proposition.

### 2. Tailwind CSS v4 Compilation Integrity
Because the boilerplate uses **Tailwind CSS v4** and **Next.js 16 (Turbopack)**, you MUST adhere to the following file configurations to prevent styling compilation failures:
* **`globals.css` structure**:
  - Start with `@import "tailwindcss";` instead of the old `@tailwind` directives.
  - Include explicit `@source` paths pointing to `src` files relative to CWD so that Turbopack compiles utilities from `page.tsx`:
    ```css
    @import "tailwindcss";
    @source "src/**/*.{ts,tsx,js,jsx}";
    @source "./src/**/*.{ts,tsx,js,jsx}";
    @source "../**/*.{ts,tsx,js,jsx}";
    @source "../../src/**/*.{ts,tsx,js,jsx}";
    @source "./src/app/**/*.{ts,tsx,js,jsx}";
    @source "./src/components/**/*.{ts,tsx,js,jsx}";
    ```
  - Define custom color variables and fonts inside the `@theme` directive (CSS-first config) instead of `tailwind.config.js`.
  - Ensure any custom generation script does not overwrite `globals.css` with deprecated v3 `@tailwind base;` directives.
* **`postcss.config.js`**: Must use CommonJS format and reference `@tailwindcss/postcss` and `autoprefixer`:
  ```javascript
  module.exports = {
    plugins: {
      "@tailwindcss/postcss": {},
      "autoprefixer": {},
    },
  };
  ```
* **`tailwind.config.js`**: Maintain a legacy `tailwind.config.js` file defining the scan content array to guarantee Webpack/Turbopack compatibility:
  ```javascript
  module.exports = {
    content: ["./src/app/**/*.{js,ts,jsx,tsx}", "./src/components/**/*.{js,ts,jsx,tsx}"],
  };
  ```

### 3. URL & Link Integrity Rule
**NEVER use dummy links** (e.g. `#` or `javascript:void(0)`) on buttons or anchor tags.
- For every CTA, check if the business profile has a real URL.
- If not, prompt the user: *"Would you like to provide a real URL for this button (e.g. booking page, shop link), or should we create a dedicated sub-page (e.g., /book, /shop), or hide the button?"*
- If the user chooses to create a dedicated page, build a simple sub-page route in the Next.js app (e.g. `src/app/book/page.tsx` with a contact form or booking schedule) and link it.

### 4. Premium Visual Aesthetics & Mobile-First Design
To ensure the user is "wowed" at first glance, follow these styling principles:
* **Rich Hero Backgrounds**: Do not use plain white or flat gray backgrounds. Inject a radial/conic gradient overlay (`bg-[radial-gradient(ellipse_at_center,var(--primary-glow),transparent)]`), subtle SVG background patterns, or generate a stunning hero background image using the `generate_image` tool.
* **Glassmorphism**: Use frosted-glass panels (`bg-white/60 backdrop-blur-md border border-white/20 shadow-sm`) for cards and floating navigation bars.
* **Micro-Animations**: Add `BorderBeam` on featured components, smooth hover state triggers (`hover:scale-[1.02] active:scale-95 transition-all duration-300`), and standard `BlurFade` entrance animations.
* **Mobile-First Layouts**: Use fluid containers with responsive paddings (`px-4 py-16 md:px-8 md:py-28`) and grid layouts that stack cleanly on phones (`grid grid-cols-1 md:grid-cols-3`).
* **Preventing Vertical Layout Gaps & Scroll Issues**:
  - **AVOID using the `TextReveal` component from Magic UI**. It introduces complex scroll-driven, sticky-positioned viewport-sized tracks (`min-h-[120vh]` and `sticky`) that frequently fail to render correctly, leaving giant empty white space gaps or breaking natural scrolling behavior.
  - Instead, use a static, beautifully stylized section (e.g. using a premium serif font, italicized styling, and subtle `BlurFade` entrance animation) to showcase mindfulness/power quotes. Standard HTML/CSS layout blocks are much more robust, responsive, and reliable.

---

## Workflow Steps

### Step 1: Business Profile & Lean Canvas Synthesis
1. Check if the unified profile directory exists. If not, prompt the user to select or initialize a profile (e.g. 'default').
2. Read the profile's `state.json` and any `LEAN_CANVAS.md` files.
3. If profile info, business name, logo, or key value propositions are missing:
   - Ask: *"Would you like to run /grill-biz to generate a Lean Canvas, /grill-name to brainstorm a name, or /grill-logo to design a logo first? Or should we fill them out together now?"*
4. Extract key components from the Lean Canvas (Problem, Solution, UVP, Revenue/Pricing).

### Step 2: Interactive Design & Layout Stepper (Grill-Me Style)
1. Present the user with an interactive checklist of proposed homepage sections based on their business profile:
   - **Hero Section** (UVP, Tagline, Primary CTA, Background Gradient/Glow)
   - **Bento Grid Features** (Core solutions and benefits)
   - **Scroll Text Reveal** (A slow-down mindfulness hook or power statement)
   - **Pricing Tiers / Packages** (Service plans or seat rates)
   - **Testimonials / Partners Marquee** (Social proof scrolling banner)
   - **FAQ Accordion** (Common customer questions)
   - **Contact Form / Newsletter** (Capture lead information)
2. Ask the user to multi-select which sections they want to compile into their landing page.
3. Once the sections are selected, review them **one-by-one** with the user. Present the copy details (e.g., hero headline text, pricing plan prices, FAQ questions) and confirm:
   - Visual style/color palette preferences (e.g. Sage Green, Luxury Dark Gold, Tech Neon Blue).
   - Real destination URLs for each section's buttons/links (applying the **URL & Link Integrity Rule**).

### Step 3: Next.js Site Generation
1. Copy the profile's logo file to the public assets directory.
2. Write `src/app/layout.tsx` with optimized SEO tags and load modern Google Fonts via `@next/font/google`.
3. Write `src/app/globals.css` using the theme config, animations, and Tailwind v4 directives.
4. Write `src/app/page.tsx` and any required sub-pages (e.g. dedicated forms or booking sheets chosen in the URL integrity step) to implement the approved layout structure.
5. Apply rich visual aesthetics (radial gradients, glassmorphism, micro-animations) to make the page pop.

### Step 4: Verification & Cloudflare Deployment
1. Run `npm run build` inside the boilerplate to verify successful static compilation.
2. If compilation fails, trace errors (PostCSS loader logs, Tailwind syntax) and fix them immediately.
3. Ask the user for their preferred Cloudflare Pages deployment option (API Token, Wrangler Login, or Drag & Drop).
   - If they prefer local deployment, assist them in running:
     `./grill-home/scripts/deploy.sh grill-home/boilerplate/out [project_name]`
4. Deploy the site, verify the live URL in the browser, capture a full-page screenshot, and present it to the user.

### Step 5: Feedback Loop & Refinement
1. Present the live URL. Ask: *"Would you like to refine the copy, adjust section backgrounds, or tweak animations?"*
2. Regenerate/recompile as requested until the user is fully satisfied.
3. At the end of the session, invite the user to submit feedback to improve GrillBiz by generating a PII-scrubbed Markdown issue block for GitHub.
