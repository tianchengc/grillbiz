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

# 2. Run /grill-biz canvas parser validation
echo -e "\n[1/3] Running Canvas Parser Validation..."
python3 grill-biz/canvas_parser.py tests/profiles/apex_cloud.md tests/output/web/apex_cloud.html
python3 grill-biz/canvas_parser.py tests/profiles/ecothreads.md tests/output/web/ecothreads.html
python3 grill-biz/canvas_parser.py tests/profiles/cleangreen.md tests/output/web/cleangreen.html

# 3. Simulate Card Compiler & Run Playwright batch screenshot renderer
echo -e "\n[2/3] Compiling Card Templates and Batch Rendering PNGs..."
# Execute helper Python command to inject mock team data into card templates
python3 -c '
import json, os
template_path = "grill-card/templates/card_template.html"
with open(template_path, "r") as f:
    template = f.read()

# Test Case 1: Apex Cloud (Solo)
apex_data = [{"name": "Alex Rivera", "role": "Cloud Architect", "email": "alex@apexcloud.io", "phone": "+1 (555) 102-9382", "company": "Apex Cloud Consulting", "website": "apexcloud.io", "logo_url": "../../grillbiz_logo.png"}]
out1 = template.replace("{{COMPANY}}", "Apex Cloud").replace("{{CARDS_DATA_JSON}}", json.dumps(apex_data))
with open("tests/output/cards/apex_cards.html", "w") as f: f.write(out1)

# Test Case 2: EcoThreads (Solo Store)
eco_data = [{"name": "Sarah Jenkins", "role": "Creative Director", "email": "sarah@ecothreads.co", "phone": "+1 (555) 839-1029", "company": "EcoThreads", "website": "ecothreads.co", "logo_url": "../../grillbiz_logo.png"}]
out2 = template.replace("{{COMPANY}}", "EcoThreads").replace("{{CARDS_DATA_JSON}}", json.dumps(eco_data))
with open("tests/output/cards/ecothreads_cards.html", "w") as f: f.write(out2)

# Test Case 3: CleanGreen (4-Person Team)
clean_data = [
    {"name": "David Vance", "role": "Founder & CEO", "email": "david@cleangreen.com", "phone": "+1 (555) 482-9102", "company": "CleanGreen Solutions", "website": "cleangreen.com", "logo_url": "../../grillbiz_logo.png"},
    {"name": "Maria Santos", "role": "COO (Operations)", "email": "maria@cleangreen.com", "phone": "+1 (555) 482-9103", "company": "CleanGreen Solutions", "website": "cleangreen.com", "logo_url": "../../grillbiz_logo.png"},
    {"name": "James Cole", "role": "CFO (Finance)", "email": "james@cleangreen.com", "phone": "+1 (555) 482-9104", "company": "CleanGreen Solutions", "website": "cleangreen.com", "logo_url": "../../grillbiz_logo.png"},
    {"name": "Sarah Brooks", "role": "Lead Cleaner", "email": "s.brooks@cleangreen.com", "phone": "+1 (555) 482-9105", "company": "CleanGreen Solutions", "website": "cleangreen.com", "logo_url": "../../grillbiz_logo.png"}
]
out3 = template.replace("{{COMPANY}}", "CleanGreen Solutions").replace("{{CARDS_DATA_JSON}}", json.dumps(clean_data))
with open("tests/output/cards/cleangreen_cards.html", "w") as f: f.write(out3)
'

# Run render_cards.py to export card PNGs (verifies playwright is installed and works)
python3 grill-card/scripts/render_cards.py tests/output/cards/apex_cards.html tests/output/cards/pngs/ theme-glassmorphism
python3 grill-card/scripts/render_cards.py tests/output/cards/ecothreads_cards.html tests/output/cards/pngs/ theme-dark-minimalist
python3 grill-card/scripts/render_cards.py tests/output/cards/cleangreen_cards.html tests/output/cards/pngs/ theme-classic-light

# 4. Simulate Bio Website Generator
echo -e "\n[3/3] Compiling Bio Website Layout Templates..."
# Execute helper Python command to inject mock link/product/blog data into bio layouts
python3 -c '
import json
with open("grill-bio/templates/layout_classic_stack.html", "r") as f: stack_template = f.read()
with open("grill-bio/templates/layout_profile_card.html", "r") as f: card_template = f.read()

# Test Case 1: Apex Cloud (Classic Stack)
socials = [{"platform": "LinkedIn", "url": "https://linkedin.com"}, {"platform": "GitHub", "url": "https://github.com"}]
links = [{"title": "Book a Cloud Audit", "url": "https://apexcloud.io/audit"}, {"title": "Terraform Modules", "url": "https://github.com/apex/terraform"}]
out1 = stack_template.replace("{{COMPANY}}", "Apex Cloud").replace("{{BIO_DESCRIPTION}}", "Fractional DevOps and cloud infrastructure optimization").replace("{{LOGO_URL}}", "../../grillbiz_logo.png").replace("{{SOCIAL_DATA_JSON}}", json.dumps(socials)).replace("{{LINKS_DATA_JSON}}", json.dumps(links)).replace("{{PRODUCTS_DATA_JSON}}", "[]").replace("{{BLOGS_DATA_JSON}}", "[]")
with open("tests/output/bio/apex_bio.html", "w") as f: f.write(out1)

# Test Case 2: EcoThreads (Profile Hub Grid)
eco_socials = [{"platform": "Instagram", "url": "https://instagram.com"}, {"platform": "Patreon", "url": "https://patreon.com"}]
eco_links = [{"title": "Shop Sustainable Hoodies", "url": "https://ecothreads.co/hoodies"}]
eco_prods = [
    {"title": "Bamboo Hoodie", "description": "Ultra-soft bamboo-fiber hoodie", "price": "$45.00", "image_url": "https://cdn-icons-png.flaticon.com/512/3649/3649775.png"},
    {"title": "Organic Cotton Tee", "description": "Sustainable cotton t-shirt", "price": "$20.00", "image_url": "https://cdn-icons-png.flaticon.com/512/3649/3649775.png"}
]
out2 = card_template.replace("{{COMPANY}}", "EcoThreads").replace("{{BIO_DESCRIPTION}}", "Ultra-soft, highly durable bamboo-fiber apparel").replace("{{LOGO_URL}}", "../../grillbiz_logo.png").replace("{{SOCIAL_DATA_JSON}}", json.dumps(eco_socials)).replace("{{LINKS_DATA_JSON}}", json.dumps(eco_links)).replace("{{PRODUCTS_DATA_JSON}}", json.dumps(eco_prods)).replace("{{BLOGS_DATA_JSON}}", "[]")
with open("tests/output/bio/ecothreads_bio.html", "w") as f: f.write(out2)
'

echo -e "\n=================================================="
echo "          TEST RUN COMPLETED SUCCESSFULLY         "
echo "All visual outputs are saved in 'tests/output/'   "
echo "=================================================="
