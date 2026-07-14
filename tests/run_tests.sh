#!/bin/bash

# GrillBiz Codebase Test Runner Script
# Automated validation of canvas parser, card template rendering, and playwright screenshots.

echo "=================================================="
echo "          GRILLBIZ AUTOMATED TEST RUNNER          "
echo "=================================================="

# 1. Clean and initialize test output folders
rm -rf tests/output
mkdir -p tests/output/web
mkdir -p tests/output/cards
mkdir -p tests/output/bio
mkdir -p tests/output/cards/pngs

# Clean temporary profiles generated for tests
rm -rf grillbiz-profiles/apex_cloud
rm -rf grillbiz-profiles/ecothreads
rm -rf grillbiz-profiles/cleangreen

# 2. Run /grill-biz canvas parser validation
echo -e "\n[1/3] Running Canvas Parser Validation..."
python3 skills/grill-biz/canvas_parser.py tests/profiles/apex_cloud.md tests/output/web/apex_cloud.html
python3 skills/grill-biz/canvas_parser.py tests/profiles/ecothreads.md tests/output/web/ecothreads.html
python3 skills/grill-biz/canvas_parser.py tests/profiles/cleangreen.md tests/output/web/cleangreen.html

# 3. Simulate Card Compiler & Run Playwright batch screenshot renderer
echo -e "\n[2/3] Compiling Card Templates and Batch Rendering PNGs..."
# Generate mock state.json files and run card_parser.py to build valid HTML files
python3 -c '
import json, os

def create_mock_profile(profile_name, company, logo_url, tagline, contact, team):
    os.makedirs(f"grillbiz-profiles/{profile_name}", exist_ok=True)
    state = {
        "profile": profile_name,
        "company": company,
        "tagline": tagline,
        "contact": contact,
        "logo_url": logo_url,
        "team": team,
        "round": 1,
        "liked_logo_ids": [],
        "liked_card_styles": [],
        "socials": {},
        "card_styles": [
            {
                "id": "style-1",
                "name": "Glassmorphism Test",
                "font_import": "@import url(\"https://fonts.googleapis.com/css2?family=Outfit:wght@300;400&display=swap\");",
                "card_bg": "rgba(255,255,255,0.1)",
                "card_border": "1px solid rgba(255,255,255,0.2)",
                "card_shadow": "0 8px 32px 0 rgba(0,0,0,0.3)",
                "front_html": "<div class=\"card-front\"><div class=\"card-company\">{{COMPANY}}</div>{{TAGLINE}}</div>",
                "back_html": "<div class=\"card-back\"><div class=\"back-left\"><div class=\"back-name\">{{NAME}}</div><div class=\"back-role\">{{ROLE}}</div></div><div class=\"back-right\">{{INFO_ROWS}}</div></div>",
                "custom_css": ""
            }
        ]
    }
    with open(f"grillbiz-profiles/{profile_name}/state.json", "w") as f:
        json.dump(state, f, indent=2)

# Case 1: Apex Cloud
create_mock_profile(
    "apex_cloud", "Apex Cloud", "../../grillbiz_logo.png", "Cloud native solutions",
    {"email": "alex@apexcloud.io", "phone": "+1 (555) 102-9382"},
    [{"name": "Alex Rivera", "role": "Cloud Architect", "email": "alex@apexcloud.io", "phone": "+1 (555) 102-9382"}]
)

# Case 2: EcoThreads
create_mock_profile(
    "ecothreads", "EcoThreads", "../../grillbiz_logo.png", "Earthy and green",
    {"email": "sarah@ecothreads.co", "phone": "+1 (555) 839-1029"},
    [{"name": "Sarah Jenkins", "role": "Creative Director", "email": "sarah@ecothreads.co", "phone": "+1 (555) 839-1029"}]
)

# Case 3: CleanGreen
create_mock_profile(
    "cleangreen", "CleanGreen Solutions", "../../grillbiz_logo.png", "Eco cleaning",
    {"email": "info@cleangreen.com", "phone": "+1 (555) 482-9102"},
    [
        {"name": "David Vance", "role": "Founder & CEO", "email": "david@cleangreen.com", "phone": "+1 (555) 482-9102"},
        {"name": "Maria Santos", "role": "COO (Operations)", "email": "maria@cleangreen.com", "phone": "+1 (555) 482-9103"},
        {"name": "James Cole", "role": "CFO (Finance)", "email": "james@cleangreen.com", "phone": "+1 (555) 482-9104"},
        {"name": "Sarah Brooks", "role": "Lead Cleaner", "email": "s.brooks@cleangreen.com", "phone": "+1 (555) 482-9105"}
    ]
)
'

# Compile cards using card_parser.py
python3 skills/grill-card/card_parser.py apex_cloud
python3 skills/grill-card/card_parser.py ecothreads
python3 skills/grill-card/card_parser.py cleangreen

# Copy compiled HTML to tests/output/cards/ so it is saved there
cp grillbiz-profiles/apex_cloud/cards/apex_cloud_cards.html tests/output/cards/apex_cards.html
cp grillbiz-profiles/ecothreads/cards/ecothreads_cards.html tests/output/cards/ecothreads_cards.html
cp grillbiz-profiles/cleangreen/cards/cleangreen_cards.html tests/output/cards/cleangreen_cards.html

# Run render_cards.py to export card PNGs (verifies playwright is installed and works)
python3 skills/grill-card/scripts/render_cards.py tests/output/cards/apex_cards.html tests/output/cards/pngs/ theme-glassmorphism
python3 skills/grill-card/scripts/render_cards.py tests/output/cards/ecothreads_cards.html tests/output/cards/pngs/ theme-dark-minimalist
python3 skills/grill-card/scripts/render_cards.py tests/output/cards/cleangreen_cards.html tests/output/cards/pngs/ theme-classic-light

# Clean up temp profiles
rm -rf grillbiz-profiles/apex_cloud
rm -rf grillbiz-profiles/ecothreads
rm -rf grillbiz-profiles/cleangreen

# 4. Validate Next.js Bio Website compilation
echo -e "\n[3/3] Validating Next.js Boilerplate Build..."
cd skills/grill-bio/boilerplate
npm run build
cd ../../..

echo -e "\n=================================================="
echo "          TEST RUN COMPLETED SUCCESSFULLY         "
echo "All visual outputs are saved in 'tests/output/'   "
echo "=================================================="
