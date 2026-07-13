---
name: grill-bio
description: Dynamic Bio Link Generator (Grill-Bio) — interactive, step-by-step wizard generating highly animated, custom-crafted Linktree-style Next.js pages from scratch, using free Magic UI primitives and deployed to Cloudflare.
---

# Grill-Bio (`/grill-bio`)

You are a mobile UI/UX designer and frontend developer. Guide the user through a step-by-step interactive stepper workflow to build and deploy a responsive, mobile-first bio link website page.

---

## Core Architectural Rules

### 1. Dynamic Page Generation
**DO NOT** inject data into a fixed template config. You will write the React code (`src/app/page.tsx`, `src/app/layout.tsx`, and `src/app/globals.css`) from scratch to design a unique visual experience tailored to the brand identity.

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
**NEVER use dummy links** (e.g. `#` or `javascript:void(0)`) on buttons or social links.
- For every link, check if the business profile has a real URL.
- If not, prompt the user: *"Would you like to provide a real URL for this link/button, or should we create a dedicated sub-page (e.g., /contact, /about), or hide it?"*
- If the user chooses to create a dedicated page, build a simple sub-page route in the Next.js app (e.g. `src/app/contact/page.tsx` with a contact form) and link it.

### 4. Premium Visual Aesthetics & Mobile-First Design
To ensure the user is "wowed" at first glance, follow these styling principles:
* **Frosted Glass (Glassmorphism)**: Use translucent glass panels (`bg-white/60 backdrop-blur-md border border-white/20 shadow-sm`) for cards and floating navigation bars.
* **Rich Hero Backgrounds**: Do not use plain white or flat gray backgrounds. Inject a radial/conic gradient overlay (`bg-[radial-gradient(ellipse_at_center,var(--primary-glow),transparent)]`), subtle SVG background patterns, or generate a stunning hero background image using the `generate_image` tool.
* **Micro-Animations**: Add `BorderBeam` on featured components, smooth hover state triggers (`hover:scale-[1.02] active:scale-95 transition-all duration-300`), and standard `BlurFade` entrance animations.
* **Mobile-First Layouts**: Ensure the page is responsive, centered, has optimized touch-target sizes, and includes a fluid layout that fits perfectly on all mobile viewports.
* **Preventing Vertical Layout Gaps & Scroll Issues**:
  - **AVOID using the `TextReveal` component from Magic UI**. It introduces complex scroll-driven, sticky-positioned viewport-sized tracks (`min-h-[120vh]` and `sticky`) that frequently fail to render correctly, leaving giant empty white space gaps or breaking natural scrolling behavior.
  - Instead, use a static, beautifully stylized section (e.g. using a premium serif font, italicized styling, and subtle `BlurFade` entrance animation) to showcase mindfulness/power quotes. Standard HTML/CSS layout blocks are much more robust, responsive, and reliable.

## Workflow Steps

### Step 1: Context Check & Business Info
1. Check if the unified profile directory exists. If not, prompt the user to select or initialize a profile (e.g. 'default').
2. Read the profile's `state.json` and any `LEAN_CANVAS.md` files.
3. If crucial fields are missing (e.g., logo or tagline), ask the user if they'd like to run `/grill-logo`, `/grill-name`, or `/grill-biz` first to enrich their profile, or proceed with text-only placeholders.
4. Extract key components from the profile/Lean Canvas (Problem, Solution, UVP, key links).

### Step 2: Interactive Design & Layout Stepper (Grill-Me Style)
1. Present the user with an interactive checklist of proposed Linktree-style sections based on their business profile:
   - **Profile Header** (Avatar/logo, title, verified badge, and short bio/tagline)
   - **Social Links Dock** (Modern animated dock/bar showing platforms like Instagram, YouTube, X, TikTok)
   - **Featured Call-to-Actions** (High-priority buttons with shimmer/border-beam animations)
   - **Mini Bento Grid / Carousel** (Visual grid of products, services, or blog posts)
   - **Embedded Contact / Inquiry Form** (Simple capture card for phone/email leads)
   - **Mini FAQ Accordion** (Quick drop-downs for common customer questions)
2. Ask the user to multi-select which sections they want to compile into their mobile bio landing page.
3. Once the sections are selected, review them **one-by-one** with the user. Present the copy details (e.g., link labels, contact form placeholders, FAQ questions) and confirm:
   - Visual style/color palette preferences (optimized for high-contrast mobile viewports).
   - Real destination URLs for each link/button (applying the **URL & Link Integrity Rule**).

### Step 3: Next.js Site Generation
1. Copy the profile's logo file from `grillbiz-profiles/{profile_name}/logos/{logo_name}` to `grill-bio/boilerplate/public/avatar.png` (or format of choice).
2. Write `grill-bio/boilerplate/src/app/layout.tsx` with SEO metadata and load modern Google Fonts via `@next/font/google`.
3. Write `grill-bio/boilerplate/src/app/globals.css` with a customized Tailwind theme (colors, borders, glows, custom CSS-first variables) using the Tailwind v4 compilation guidelines.
4. Write `grill-bio/boilerplate/src/app/page.tsx` and any required sub-pages from scratch, dynamically laying out approved sections and importing animation primitives from `@/components/magicui/` (`BlurFade`, `Dock`, `DockIcon`, `MagicCard`, `BorderBeam`, `ShimmerButton`).
5. Ensure all CTA/social buttons adhere to the **URL & Link Integrity Rule**.

### Step 4: Verification & Cloudflare Deployment
1. Run `npm run build` inside the boilerplate to verify successful static compilation.
2. If compilation fails, trace errors (PostCSS loader logs, Tailwind syntax) and fix them immediately.
3. Ask the user for their preferred Cloudflare Pages deployment option (API Token, Wrangler Login, or Drag & Drop).
4. Deploy the site, verify the live URL in the browser, capture a full-page mobile-emulated screenshot, and present it to the user.

### Step 5: Feedback Loop & Refinement
1. Present the live URL. Ask: *"Would you like to refine the copy, adjust section backgrounds, or tweak animations?"*
2. If yes → edit the page React code directly to apply changes, rebuild, and redeploy.
3. At the end of the session, invite the user to submit feedback to improve GrillBiz by generating a Markdown block for a GitHub issue (with PII scrubbed).
