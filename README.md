# GrillBiz (Business Helper Skills Bundle)

Welcome to **GrillBiz**, a premium bundle of open-source business helper skills designed for AI coding assistants like Claude Code and Antigravity. GrillBiz equips solo developers, indie hackers, and founders with structured workflows to bootstrap and manage businesses directly from their terminal—putting every business asset through a thorough vetting "grill."

---

## Skills Included

### 1. 🏷️ Naming Skill: Grill-Name (Command: `/grill-name`)
* **Path:** `grill-name/`
* **Features:** Guided 3-stage brand analysis (using neologisms, suggestive metaphors, and compounds), domain checking (prioritizing available `.com` domains), automated DNS/HTTP checks, raw socket WHOIS queries, trademark risk scanning, and registrar link routing.
* **Usage:** `/grill-name [count=5] [domain_check=true]`

### 2. 📇 Business Card Skill (Command: `/grill-card` - Pending)
* **Path:** `business-card/`
* **Features:** Modern HTML/CSS business card templates (glassmorphism, minimalist dark mode) with a built-in 'Save as PNG' button and Playwright CLI rendering tool.

### 3. 🌳 Linktree-like Bio Website Skill (Command: `/grill-bio` - Pending)
* **Path:** `linktree/`
* **Features:** Generates a fully responsive, animated static personal/company bio page matching the styling of the generated business card.

### 4. 📸 Instagram Post Skill (Command: `/grill-post` - Pending)
* **Path:** `instagram/`
* **Features:** Automates visual content generation and posts directly to Instagram Business accounts using the Instagram Graph API.

### 5. 🔮 Jiuzilihuo Fengshui Skill (Command: `/grill-fengshui` - Pending)
* **Path:** `jiuzilihuo/`
* **Features:** Evaluates project alignment with Period 9 (9-Purple-Fire) energy using industry profiles, color design matching, and Bazi birth chart compatibility calculations.

### 6. 🤝 B Corp Skill (Command: `/grill-bcorp` - Pending)
* **Path:** `b-corp/`
* **Features:** Interactive tracker guiding you through B Impact Assessment (BIA) pillars and providing customized company policy templates.

---

## Monetization Model (100% Affiliate-Based)
GrillBiz is completely free and client-side. The bundle generates revenue via domain registration affiliate commission links (supporting Namecheap) embedded in the `/grill-name` output.
* **Configuration:** Register as a Namecheap affiliate on Impact Radius or CJ, obtain your affiliate ID, and set the `NAMECHEAP_AFFILIATE_ID` environment variable. The checking script will automatically append your affiliate code to domain links.
* If you want to register at wholesale prices without supporting the project, direct at-cost Cloudflare Registrar links are also output in the results.
