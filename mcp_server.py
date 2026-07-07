#!/usr/bin/env python3
import sys
import os
import subprocess
import json

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Error: 'mcp' package is not installed. Please run 'pip install mcp'")
    sys.exit(1)

# Initialize FastMCP Server
mcp = FastMCP("grillbiz", version="1.1.0")

# ==========================================================
# 🛠️ MCP TOOLS (Action Executions)
# ==========================================================

@mcp.tool()
def check_domain(domain: str) -> str:
    """
    Check if a specific domain is available or taken using DNS, WHOIS, and HTTP checks.
    
    Args:
        domain: The domain name to check (e.g. 'google.com').
    """
    script_path = os.path.join(os.path.dirname(__file__), "grill-name", "check_domain.py")
    try:
        res = subprocess.run(
            [sys.executable, script_path, domain],
            capture_output=True, text=True, check=True
        )
        return res.stdout
    except Exception as e:
        return f"Error checking domain: {str(e)}"

@mcp.tool()
def compile_lean_canvas(profile_path: str, output_path: str) -> str:
    """
    Parse a Lean Canvas markdown profile and compile it into a visual grid HTML page.
    
    Args:
        profile_path: Absolute path to the source markdown profile.
        output_path: Absolute path to write the compiled HTML page to.
    """
    script_path = os.path.join(os.path.dirname(__file__), "grill-biz", "canvas_parser.py")
    try:
        res = subprocess.run(
            [sys.executable, script_path, profile_path, output_path],
            capture_output=True, text=True, check=True
        )
        return res.stdout
    except Exception as e:
        return f"Error compiling canvas: {str(e)}"

@mcp.tool()
def generate_business_card_page(company: str, cards_data_json: str, output_path: str) -> str:
    """
    Generate the HTML business card list page by injecting team member details into the card template.
    
    Args:
        company: The name of the company.
        cards_data_json: JSON string of team members. Format: [{"name": "Jane", "role": "CEO", "email": "j@co.com", "phone": "+1...", "company": "Co", "website": "co.com", "logo_url": "..."}]
        output_path: Absolute path to write the compiled cards HTML file to.
    """
    template_path = os.path.join(os.path.dirname(__file__), "grill-card", "templates", "card_template.html")
    if not os.path.exists(template_path):
        return f"Error: Card template not found at {template_path}"
    
    try:
        # Validate JSON string
        json.loads(cards_data_json)
        
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        content = content.replace("{{COMPANY}}", company)
        content = content.replace("{{CARDS_DATA_JSON}}", cards_data_json)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"Success: Generated business card HTML page at {output_path}"
    except json.JSONDecodeError:
        return "Error: Invalid JSON format for 'cards_data_json'."
    except Exception as e:
        return f"Error generating business cards page: {str(e)}"

@mcp.tool()
def render_business_cards(html_path: str, output_dir: str, theme: str = "theme-glassmorphism") -> str:
    """
    Open the generated HTML business card list page using Playwright and export high-res PNG crops of each card.
    
    Args:
        html_path: Absolute path to the cards HTML file.
        output_dir: Absolute path to the directory to save the cropped PNGs to.
        theme: Theme name ('theme-glassmorphism', 'theme-dark-minimalist', 'theme-gradient-bold', 'theme-classic-light').
    """
    script_path = os.path.join(os.path.dirname(__file__), "grill-card", "scripts", "render_cards.py")
    try:
        res = subprocess.run(
            [sys.executable, script_path, html_path, output_dir, theme],
            capture_output=True, text=True, check=True
        )
        return res.stdout
    except Exception as e:
        return f"Error rendering cards: {str(e)}"

@mcp.tool()
def generate_bio_page(
    company: str,
    bio_description: str,
    logo_url: str,
    social_data_json: str,
    links_data_json: str,
    products_data_json: str,
    blogs_data_json: str,
    layout_name: str,
    output_path: str
) -> str:
    """
    Generate a mobile-first Instagram bio link website page.
    
    Args:
        company: The name of the company.
        bio_description: A short 1-2 sentence tagline/description.
        logo_url: URL or local path to the company logo.
        social_data_json: JSON string of social links. Format: [{"platform": "OnlyFans", "url": "https://..."}]
        links_data_json: JSON string of primary CTA links. Format: [{"title": "Shop", "url": "https://..."}]
        products_data_json: JSON string of products. Format: [{"title": "P1", "description": "D1", "price": "$10", "image_url": "..."}]
        blogs_data_json: JSON string of blog posts. Format: [{"title": "B1", "description": "D1", "url": "...", "image_url": "..."}]
        layout_name: Layout template style name ('classic_stack' or 'profile_card').
        output_path: Absolute path to write the compiled bio HTML page to.
    """
    # Select template file
    layout_file = "layout_classic_stack.html" if layout_name == "classic_stack" else "layout_profile_card.html"
    template_path = os.path.join(os.path.dirname(__file__), "grill-bio", "templates", layout_file)
    
    if not os.path.exists(template_path):
        return f"Error: Layout template '{layout_name}' not found at {template_path}"
        
    try:
        # Validate all JSON inputs
        json.loads(social_data_json)
        json.loads(links_data_json)
        json.loads(products_data_json)
        json.loads(blogs_data_json)
        
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        content = content.replace("{{COMPANY}}", company)
        content = content.replace("{{BIO_DESCRIPTION}}", bio_description)
        content = content.replace("{{LOGO_URL}}", logo_url)
        content = content.replace("{{SOCIAL_DATA_JSON}}", social_data_json)
        content = content.replace("{{LINKS_DATA_JSON}}", links_data_json)
        content = content.replace("{{PRODUCTS_DATA_JSON}}", products_data_json)
        content = content.replace("{{BLOGS_DATA_JSON}}", blogs_data_json)
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"Success: Generated mobile bio page ({layout_name}) at {output_path}"
    except json.JSONDecodeError as je:
        return f"Error: Invalid JSON input format: {str(je)}"
    except Exception as e:
        return f"Error generating bio page: {str(e)}"


# ==========================================================
# 🧠 MCP PROMPTS (Workflow Steppers & Instructions)
# ==========================================================

def _read_skill_instructions(skill_folder: str) -> str:
    path = os.path.join(os.path.dirname(__file__), skill_folder, "SKILL.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return f"Error: Instructions for skill '{skill_folder}' not found."

@mcp.prompt()
def grill_biz_workflow() -> str:
    """Load the Grill-Biz strategic business canvas stepper instructions to guide the Lean Canvas interview."""
    return _read_skill_instructions("grill-biz")

@mcp.prompt()
def grill_name_workflow() -> str:
    """Load the Grill-Name brand creation and domain verification guidelines."""
    return _read_skill_instructions("grill-name")

@mcp.prompt()
def grill_post_workflow() -> str:
    """Load the Grill-Post social media draft and automated API publishing workflow."""
    return _read_skill_instructions("grill-post")

@mcp.prompt()
def grill_card_workflow() -> str:
    """Load the Grill-Card business card generation stepper instructions."""
    return _read_skill_instructions("grill-card")

@mcp.prompt()
def grill_bio_workflow() -> str:
    """Load the Grill-Bio mobile bio link website builder and deployment workflow."""
    return _read_skill_instructions("grill-bio")


if __name__ == "__main__":
    mcp.run()
