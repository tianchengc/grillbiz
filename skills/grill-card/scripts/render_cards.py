#!/usr/bin/env python3
import sys
import os
import time

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Error: Playwright is not installed. Run 'pip install playwright' and 'playwright install'")
    sys.exit(1)

def render_cards(html_path, output_dir, theme="theme-glassmorphism"):
    """
    Open the generated HTML business card list using Playwright,
    select the theme, and batch-export each card's front/back as high-res PNGs.
    """
    if not os.path.exists(html_path):
        print(f"Error: HTML cards file not found at {html_path}")
        sys.exit(1)

    os.makedirs(output_dir, exist_ok=True)
    abs_html_path = os.path.abspath(html_path)

    print(f"Initializing Playwright to render cards with theme '{theme}'...")
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1400, "height": 1000})
        
        # Navigate to local file
        page.goto(f"file://{abs_html_path}")
        
        # Select theme in the page
        page.evaluate(f"document.body.className = '{theme}';")
        
        # Remove scaling transforms on business cards to screenshot them at full 1050x600px resolution
        page.evaluate("""
            document.querySelectorAll('.business-card').forEach(el => {
                el.style.transform = 'none';
                el.style.marginBottom = '0';
                // Force full resolution size
                el.style.width = '1050px';
                el.style.height = '600px';
            });
            // Hide headers/buttons during batch screenshot
            document.querySelector('header').style.display = 'none';
            document.querySelectorAll('.btn-save-card').forEach(btn => btn.style.display = 'none');
        """)
        
        # Wait a moment for fonts/layouts to render
        time.sleep(1)

        # Get all team member cards data
        cards_count = page.evaluate("cardsData.length")
        print(f"Found {cards_count} team members. Starting export...")

        for i in range(cards_count):
            member = page.evaluate(f"cardsData[{i}]")
            safe_name = member['name'].replace(" ", "_").lower()
            
            # Screenshot Front Side
            front_selector = f"#{member['frontId']}"
            front_output = os.path.join(output_dir, f"{safe_name}_front.png")
            print(f"Exporting front of {member['name']} -> {front_output}")
            page.locator(front_selector).screenshot(path=front_output, omit_background=True)

            # Screenshot Back Side
            back_selector = f"#{member['backId']}"
            back_output = os.path.join(output_dir, f"{safe_name}_back.png")
            print(f"Exporting back of {member['name']} -> {back_output}")
            page.locator(back_selector).screenshot(path=back_output, omit_background=True)

        browser.close()
    print("Success: Finished batch rendering business cards.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 render_cards.py <path_to_cards_html> <output_directory> [theme_name]")
        print("Themes: theme-glassmorphism, theme-dark-minimalist, theme-gradient-bold, theme-classic-light")
        sys.exit(1)

    html_file = sys.argv[1]
    out_dir = sys.argv[2]
    theme_arg = sys.argv[3] if len(sys.argv) >= 4 else "theme-glassmorphism"

    render_cards(html_file, out_dir, theme_arg)
