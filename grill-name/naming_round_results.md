# Naming Round Results: Diverse Branding Styles

This document records the results of the second-round naming process, specifically executed to find brand options across diverse creative styles where the high-trust **`.com`** domain name is available to register.

---

## 1. Deconstructing the Terminology (What do these words mean?)

To avoid confusing shorthand, here is a breakdown of the core terms used in these names:
* **"Co-founder":** A business partner who shares the work, strategy, and execution of launching a company. In this project, the AI agent acts as a digital co-founder.
* **"Pack" / "Kit":** Refers to a modular bundle, collection, or package of tools and instructions (like a software developer's pack).
* **"Boot":** Short for **bootstrapping**, which is starting a business with minimal external capital, relying entirely on self-funding and sweat equity.
* **"Grill":** A metaphor for questioning, testing, and examining something intensely under heat (inspired by the `/grill-me` developer command). 
* **"Biz":** Standard shorthand for business. (Because "biz" is generic and sometimes perceived as corporate jargon, we have shifted our primary recommendations away from it).

---

## 2. Naming Styles & Brand Strategy (All `.com` Available)

We ran our domain verification script `check_domain.py` to identify candidate names distributed across different branding styles where the `.com` is **100% available** for registration.

### Style A: Neologisms & Coined Words (Like Cisco, Nvidia, Google)
*Invented words that are highly unique, protectable, and easy to trademark.*
* **NomGrill (`nomgrill.com` - Available):**
  * *Meaning:* Blends **"Nom"** (from the Latin root *nomen* meaning "name") with **"Grill"** (intense questioning). Fits the developer slash-command vibe.
  * *Cloudflare At-Cost Registration Link:* [domains.cloudflare.com/?domain=nomgrill](https://domains.cloudflare.com/?domain=nomgrill)
  * *Namecheap Link:* [namecheap.com/search?q=nomgrill.com](https://www.namecheap.com/domains/registration/results/?domain=nomgrill.com)
* **Grillifi (`grillifi.com` - Available):**
  * *Meaning:* Verb-ifies **"Grill"** (using the suffix "-ify"). Modern, energetic SaaS style.
  * *Cloudflare At-Cost Registration Link:* [domains.cloudflare.com/?domain=grillifi](https://domains.cloudflare.com/?domain=grillifi)
  * *Namecheap Link:* [namecheap.com/search?q=grillifi.com](https://www.namecheap.com/domains/registration/results/?domain=grillifi.com)

### Style B: Suggestive & Metaphorical (Like Stripe, Slack, Nike)
*Real words that hint at the core benefit, structure, or guidance.*
* **Grillname (`grillname.com` - Available):**
  * *Meaning:* Direct, punchy imperative command.
  * *Cloudflare At-Cost Registration Link:* [domains.cloudflare.com/?domain=grillname](https://domains.cloudflare.com/?domain=grillname)
  * *Namecheap Link:* [namecheap.com/search?q=grillname.com](https://www.namecheap.com/domains/registration/results/?domain=grillname.com)

### Style C: Catchy Combinations (Like SpaceX, Microsoft)
*Two related concepts welded together to form a highly descriptive but punchy name.*
* **GrillBiz (`grillbiz.com` - Available):**
  * *Meaning:* "Grill" (questioning) + "Biz" (business). Directly represents vetting business ideas to see if they survive the heat.
  * *Cloudflare At-Cost Registration Link:* [domains.cloudflare.com/?domain=grillbiz](https://domains.cloudflare.com/?domain=grillbiz)
  * *Namecheap Link:* [namecheap.com/search?q=grillbiz.com](https://www.namecheap.com/domains/registration/results/?domain=grillbiz.com)
* **OpsGrill (`opsgrill.com` - Available):**
  * *Meaning:* "Ops" (Operations) + "Grill". Ideal for a helper suite that audits and tests your business operations.
  * *Cloudflare At-Cost Registration Link:* [domains.cloudflare.com/?domain=opsgrill](https://domains.cloudflare.com/?domain=opsgrill)
  * *Namecheap Link:* [namecheap.com/search?q=opsgrill.com](https://www.namecheap.com/domains/registration/results/?domain=opsgrill.com)

### Style D: Descriptive Packs (Like Salesforce, Facebook)
*Explicitly describes what the tool does, providing high clarity but less abstract branding.*
* **Co-founder Pack (`cofounderpack.com` - Available):**
  * *Meaning:* "Co-founder" (business partner sharing execution) + "Pack" (bundle of tools). Highly clear and self-explanatory.
  * *Cloudflare At-Cost Registration Link:* [domains.cloudflare.com/?domain=cofounderpack](https://domains.cloudflare.com/?domain=cofounderpack)
  * *Namecheap Link:* [namecheap.com/search?q=cofounderpack.com](https://www.namecheap.com/domains/registration/results/?domain=cofounderpack.com)

---

## 3. Registrar Pricing & Affiliate Setup

* **Cloudflare Registrar (At-Cost):**
  Cloudflare Registrar operates as an at-cost service. Because they add zero profit markup, a `.com` registration costs exactly **$10.44 USD/year** (registry fee + ICANN fee).
  *Note: Cloudflare does not offer an affiliate program. To register, use the direct dashboard search links provided above.*
* **Namecheap (Affiliate Program):**
  To generate affiliate revenue from this package, you must register as a Namecheap affiliate (via Impact Radius, CJ Affiliate, or ShareASale) and obtain your affiliate ID.
  * **Configuration:** Set your affiliate ID in the environment variable `NAMECHEAP_AFFILIATE_ID` or pass it via the CLI argument `--aff-id`.
  * **How it works:** When set, the check script automatically appends `&aff=YOUR_ID` to Namecheap URLs.
  * **Commission Rates:** Namecheap pays commissions strictly on the **first purchase made by a first-time/new customer** (renewals and existing customer purchases do not qualify):
    * **Domain Registrations:** Typically **20%** of the transaction value.
    * **Web Hosting & SSL Certificates:** Typically **35%**.
    * **VPN:** Up to **50%–53%** for annual plans.
  * **Cookie Window:** The referral cookie remains active for **30 days** after a user clicks your link. Any new user account creation and purchase during this window will be attributed to your affiliate code.
