#!/usr/bin/env python3
import sys
import os
import json

def generate_logo_html(profile_name):
    # Locate paths
    script_dir = os.path.dirname(os.path.realpath(__file__))
    workspace_dir = os.path.dirname(script_dir)
    
    # State file path
    state_dir = os.path.join(workspace_dir, "grillbiz-profiles", "logos", profile_name)
    state_file = os.path.join(state_dir, "state.json")
    
    # Check if state exists
    if not os.path.exists(state_file):
        print(f"Error: state.json not found at {state_file}")
        sys.exit(1)
        
    with open(state_file, "r", encoding="utf-8") as f:
        logos_data = json.load(f)
        
    # Read template
    template_path = os.path.join(script_dir, "templates", "logo_template.html")
    if not os.path.exists(template_path):
        print(f"Error: HTML template not found at {template_path}")
        sys.exit(1)
        
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
        
    # Build HTML blocks
    html_cards = []
    for item in logos_data:
        logo_id = item["id"]
        round_num = item["round"]
        liked = item.get("liked", False)
        # Relative path from the output HTML file
        image_src = f"{profile_name}/{os.path.basename(item['path'])}"
        
        pinned_class = "pinned" if liked else ""
        active_class = "active" if liked else ""
        active_text = "<span>❤️</span> Selected" if liked else "<span>🤍</span> Select Logo"
        
        card = f"""
            <div class="logo-card {pinned_class}">
                <div class="logo-frame">
                    <img src="{image_src}" class="logo-img" alt="{logo_id}">
                </div>
                <div class="logo-info">
                    <span class="logo-id">{logo_id.upper()}</span>
                    <span class="logo-round">Round {round_num}</span>
                </div>
                <div class="logo-actions">
                    <button id="like-btn-{logo_id}" class="like-btn {active_class}" onclick="selectLogo('{logo_id}')">
                        {active_text}
                    </button>
                    <a href="{image_src}" download="{logo_id}.png" class="download-btn" title="Download PNG">
                        <span>📥</span>
                    </a>
                </div>
            </div>"""
        html_cards.append(card)
        
    logos_html = "\n".join(html_cards)
    
    # Replace placeholders
    rendered = template
    rendered = rendered.replace("{{TITLE}}", profile_name.upper())
    rendered = rendered.replace("{{LOGOS_HTML}}", logos_html)
    
    # Write output HTML file
    output_html_path = os.path.join(workspace_dir, "grillbiz-profiles", "logos", f"{profile_name}_logos.html")
    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
    
    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(rendered)
        
    print(f"Success: Generated brand logo catalog at {output_html_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 logo_parser.py <profile_name>")
        sys.exit(1)
        
    profile_name = sys.argv[1].strip().lower()
    generate_logo_html(profile_name)

if __name__ == "__main__":
    main()
