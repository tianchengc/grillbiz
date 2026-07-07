#!/usr/bin/env python3
import sys
import os
import re

def parse_markdown(filepath):
    """
    Parse standard Lean Canvas Markdown headings and bullet points.
    Returns a dictionary of section contents.
    """
    if not os.path.exists(filepath):
        print(f"Error: Profile file not found at {filepath}")
        sys.exit(1)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # The 9 core sections mapping
    sections = {
        "problem": "",
        "segments": "",
        "uvp": "",
        "solution": "",
        "channels": "",
        "revenue": "",
        "costs": "",
        "metrics": "",
        "advantage": "",
        "alternatives": "",
        "early_adopters": "",
        "concept": ""
    }

    # Helper regex to find content under markdown headings
    # Matches ## <number>. <Title> followed by everything until the next ## or #
    pattern = r"##\s+\d+\.\s+([^#\n\r]+)([\s\S]*?)(?=(?:##\s+\d+\.)|#|$)"
    matches = re.findall(pattern, content)

    for title, text in matches:
        title_clean = title.strip().lower()
        text_clean = text.strip()

        # Parse sub-elements (like Alternatives, Early Adopters, High-Level Concept) from bullets
        bullets = []
        for line in text_clean.splitlines():
            line = line.strip()
            if not line:
                continue
            
            # Check for sub-elements starting with **
            if "alternative" in line.lower() and "**" in line:
                sections["alternatives"] = re.sub(r"^\*\s*\*\*.*?\*\*:\s*", "", line)
            elif "early adopter" in line.lower() and "**" in line:
                sections["early_adopters"] = re.sub(r"^\*\s*\*\*.*?\*\*:\s*", "", line)
            elif "concept" in line.lower() and "**" in line:
                sections["concept"] = re.sub(r"^\*\s*\*\*.*?\*\*:\s*", "", line)
            else:
                # Standard bullet point
                clean_bullet = re.sub(r"^\*\s*", "", line)
                if clean_bullet:
                    bullets.append(clean_bullet)

        bullet_html = "\n".join([f"<li>{b}</li>" for b in bullets])
        
        # Map to specific keys
        if "problem" in title_clean:
            sections["problem"] = bullet_html
        elif "segment" in title_clean:
            sections["segments"] = bullet_html
        elif "value" in title_clean:
            sections["uvp"] = bullet_html
        elif "solution" in title_clean:
            sections["solution"] = bullet_html
        elif "channel" in title_clean:
            sections["channels"] = bullet_html
        elif "revenue" in title_clean:
            sections["revenue"] = bullet_html
        elif "cost" in title_clean:
            sections["costs"] = bullet_html
        elif "metric" in title_clean:
            sections["metrics"] = bullet_html
        elif "advantage" in title_clean:
            sections["advantage"] = bullet_html

    # Extract title of the canvas
    title_match = re.search(r"#\s+Lean Canvas:\s*(.*)", content)
    canvas_title = title_match.group(1).strip() if title_match else "Lean Canvas"
    sections["title"] = canvas_title

    return sections


def generate_html(data, output_path):
    """
    Generate a beautifully styled HTML file by injecting parsed data into the HTML template.
    """
    # Locate the template file relative to this script
    script_dir = os.path.dirname(os.path.realpath(__file__))
    template_path = os.path.join(script_dir, "templates", "template.html")

    if not os.path.exists(template_path):
        print(f"Error: HTML template not found at {template_path}")
        sys.exit(1)

    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()

    # Create sub-sections HTML if values exist
    alt_html = f'<div class="sub-section"><div class="sub-title">Existing Alternatives</div><div class="sub-content">{data["alternatives"]}</div></div>' if data["alternatives"] else ''
    concept_html = f'<div class="sub-section"><div class="sub-title">High-Level Concept</div><div class="sub-content">{data["concept"]}</div></div>' if data["concept"] else ''
    adopters_html = f'<div class="sub-section"><div class="sub-title">Early Adopters</div><div class="sub-content">{data["early_adopters"]}</div></div>' if data["early_adopters"] else ''

    # Replace placeholders
    rendered = template
    rendered = rendered.replace("{{TITLE}}", data["title"])
    rendered = rendered.replace("{{PROBLEM}}", data["problem"])
    rendered = rendered.replace("{{ALTERNATIVES_HTML}}", alt_html)
    rendered = rendered.replace("{{SOLUTION}}", data["solution"])
    rendered = rendered.replace("{{METRICS}}", data["metrics"])
    rendered = rendered.replace("{{UVP}}", data["uvp"])
    rendered = rendered.replace("{{CONCEPT_HTML}}", concept_html)
    rendered = rendered.replace("{{ADVANTAGE}}", data["advantage"])
    rendered = rendered.replace("{{CHANNELS}}", data["channels"])
    rendered = rendered.replace("{{SEGMENTS}}", data["segments"])
    rendered = rendered.replace("{{EARLY_ADOPTERS_HTML}}", adopters_html)
    rendered = rendered.replace("{{COSTS}}", data["costs"])
    rendered = rendered.replace("{{REVENUE}}", data["revenue"])

    # Write output
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered)
    print(f"Success: Generated visual web canvas at {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 canvas_parser.py <profile_name_or_markdown_path> [output_html_path]")
        sys.exit(1)

    input_arg = sys.argv[1].strip()
    
    # Determine input and output paths
    if input_arg.endswith(".md"):
        profile_path = input_arg
        if len(sys.argv) >= 3:
            output_html_path = sys.argv[2].strip()
        else:
            # Default to same folder, changing extension to html
            output_html_path = os.path.splitext(profile_path)[0] + ".html"
    else:
        # Standard named profile in active workspace
        profile_name = input_arg.lower()
        profile_path = f"grillbiz-profiles/{profile_name}.md"
        if len(sys.argv) >= 3:
            output_html_path = sys.argv[2].strip()
        else:
            output_html_path = f"grillbiz-profiles/web/{profile_name}.html"

    # Process
    print(f"Parsing profile: {profile_path}...")
    canvas_data = parse_markdown(profile_path)
    generate_html(canvas_data, output_html_path)

if __name__ == "__main__":
    main()
