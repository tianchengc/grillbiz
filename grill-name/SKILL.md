---
name: grill-name
description: AI Naming Skill (Grill-Name) generating candidates across 5 naming styles, verifying .com domain status, and scanning trademark risks.
---

# Grill-Name (`/grill-name`)

Welcome to **Grill-Name**, the brand name and domain specialist.

### What does "Grill-Name" mean?
"Grill-Name" is a portmanteau of **Grill** (inspired by the `/grill-me` command) and **Name**. Instead of just generating listless combinations of words, it puts candidate names through a rigorous, heat-testing review:
1. **Diverse Style Analysis:** Generates candidates across five distinct branding styles (Abstract/Coined, Suggestive/Evocative, Tactile Metaphors, Compounds, and Descriptive).
2. **Strict Domain Grill:** Prioritizes `.com` availability, ensuring you own the primary trust and authority extension.
3. **Trademark & Litigation Grill:** Scans phonetic and spelling similarities to prevent legal trademark disputes.

---

## Skill Parameters
* `count` (integer, default: 5): The number of final, verified, available `.com` naming options to return.
* `domain_check` (boolean, default: true): If `true`, checks domain availability and returns registration details.

---

## Naming Styles & Strategy
When the user asks you to brainstorm names, you **must** categorize your generated candidates into these 5 styles, drawing inspiration from [examples.md](file://./examples.md):
1. **Abstract & Coined (Neologisms):** Entirely invented words (e.g. Google, Nvidia). Highly protectable, strong trademark potential.
2. **Suggestive & Evocative:** Real words conveying the spirit or benefits metaphorically (e.g. Stripe, Slack, Nike).
3. **Tactile Metaphors (Out-of-Context Nouns):** Organic, household objects (e.g. Apple, BlackBerry, Caterpillar) providing warmth.
4. **Compounds & Portmanteaus:** Word fragments welded together (e.g. Cisco, SpaceX, Instagram).
5. **Descriptive:** Straightforward descriptive combinations (e.g. PayPal, Salesforce).

---

## The Grill-Name Workflow

### Stage 1: Creative Brand Options Generation
1. Ask the user for their business description, values, target audience, and preferred aesthetic.
2. Generate candidate names distributed evenly across the **5 Naming Styles**. Ensure all candidates sound natural, are easy to spell, and pass the "telephone pronunciation test."

### Stage 2: Domain Verification (The TLD Trust Priority)
If `domain_check` is enabled, check candidates against the trust hierarchy:
1. **`.com` (Primary Goal):** The gold standard of customer trust and brand authority. You must search for names where the `.com` is available to avoid brand dilution and trademark confusion.
2. **Modern TLD Fallbacks (`.co`, `.io`, `.ai`):** Only consider these if the `.com` is taken and parked by speculative domain brokers demanding excessive fees.
3. **Direct Check:** Execute the [check_domain.py](file://./check_domain.py) script on the candidates:
   `python3 check_domain.py <domains...>`
4. **Affiliate & Registrar Strategy:**
   - **Cloudflare Registrar:** Directs users to register at wholesale at-cost cost (e.g. $10.44 USD/year for `.com`) via the URL `https://domains.cloudflare.com/?domain=name`.
   - **Namecheap (Affiliate Link):** Generates Namecheap purchase links. To monetize this open-source skill, users can configure their affiliate ID in the environment variable `NAMECHEAP_AFFILIATE_ID` (or via CLI `--aff-id`). If set, the link will route through their affiliate code.
5. **Loop Engineering:** Discard taken domains. If the number of available candidates is less than `count`, loop back to Stage 1 to generate fresh candidates. Repeat until you have `count` fully available `.com` domains.

### Stage 3: The Risk Grill
Evaluate the final candidate list for trademark, phonetic, and cultural risks:
* **Phonetic Litigation Risk:** Does it sound too close to a protected brand (e.g., "Figma" vs "Phigma")?
* **Trademark Conflict:** Are there direct competitors using this mark?
* **Global Meaning:** Does the name mean anything awkward, offensive, or difficult to pronounce in major foreign markets?
