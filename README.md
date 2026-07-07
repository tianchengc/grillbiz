# GrillBiz (Business Helper Skills Bundle)

Welcome to **GrillBiz**, a premium bundle of open-source business helper skills designed for AI coding assistants like Claude Code and Antigravity. GrillBiz equips solo developers, indie hackers, and founders with structured workflows to bootstrap and manage businesses directly from their terminal—putting every business asset through a thorough vetting "grill."

---

## Skills Included

### 1. 📊 Business Analysis Skill: Grill-Biz (Command: `/grill-biz`)
* **Path:** `grill-biz/`
* **Features:** Guided 9-block Lean Canvas interview, multi-profile strategy vault (`grillbiz-profiles/`), active profile copying to `LEAN_CANVAS.md`, and automated HTML visual grid exports using CSS Grid with a dark/light mode toggle.
* **Usage:** `/grill-biz [profile_name]` (e.g. `/grill-biz coffee-shop`)

### 2. 🏷️ Naming Skill: Grill-Name (Command: `/grill-name`)
* **Path:** `grill-name/`
* **Features:** Guided 3-stage brand analysis (using neologisms, suggestive metaphors, and compounds), domain checking (prioritizing available `.com` domains), automated DNS/HTTP checks, raw socket WHOIS queries, trademark risk scanning, and registrar link routing. Automatically reads `LEAN_CANVAS.md` context if present.
* **Usage:** `/grill-name [count=5] [domain_check=true]`

### 3. 📸 Instagram Post Skill: Grill-Post (Command: `/grill-post`)
* **Path:** `grill-post/`
* **Features:** Step-by-step stepper workflow (validates `.env` keys, reads `LEAN_CANVAS.md` context, drafts SEO/GEO captions, automatically queries Facebook Page Places API for location IDs, supports optional API keys for text-only drafting, and publishes live or outputs manual draft copy).
* **Usage:** `/grill-post [auto_approve=false]`

### 4. 📇 Business Card Skill: Grill-Card (Command: `/grill-card`)
* **Path:** `grill-card/`
* **Features:** Stepper workflow (checks `LEAN_CANVAS.md`), front/back design card generator, multi-member team cards generation, 4 style theme presets (Glassmorphism, Minimalist Dark, Bold Gradient, Classic Light), browser-based `html2canvas` save button, and a background Playwright CLI script (`render_cards.py`) to batch-export high-res card PNGs.
* **Usage:** `/grill-card`

### 5. 🌳 Instagram Bio Link Skill: Grill-Bio (Command: `/grill-bio`)
* **Path:** `grill-bio/`
* **Features:** Mobile-first vertical stack link page generator. Features cohesive visual themes matching business cards, a local Wrangler CLI deployment script (`deploy.sh`) supporting interactive browser login or automated `.env` API tokens, and a pre-configured GitHub Actions workflow template.
* **Usage:** `/grill-bio`

### 6. 🔮 Jiuzilihuo Fengshui Skill (Command: `/grill-fengshui` - Pending)
* **Path:** `jiuzilihuo/`
* **Features:** Evaluates project alignment with Period 9 (9-Purple-Fire) energy using industry profiles, color design matching, and Bazi birth chart compatibility calculations.

### 7. 🤝 B Corp Skill (Command: `/grill-bcorp` - Pending)
* **Path:** `b-corp/`
* **Features:** Interactive tracker guiding you through B Impact Assessment (BIA) pillars and providing customized company policy templates.

---
Impact-Site-Verification: 8d7edcdd-685d-43b8-ac05-4708d5a6fc11

