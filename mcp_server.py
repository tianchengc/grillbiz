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
mcp = FastMCP("grillbiz", version="1.2.0")

# ==========================================================
# 🛠️ MCP TOOLS (Action Executions)
# ==========================================================

@mcp.tool()
def check_domain(domain: str, tlds: str = None) -> str:
    """
    Check if a specific domain or base brand name is available or taken.
    
    Args:
        domain: The domain name or base brand name to check (e.g. 'google' or 'google.com').
        tlds: Comma-separated list of extensions to check (e.g. 'com,co,net,ca'). If omitted, uses default list.
    """
    script_path = os.path.join(os.path.dirname(__file__), "grill-name", "check_domain.py")
    cmd = [sys.executable, script_path, domain]
    if tlds:
        cmd.extend(["--tlds", tlds])
    try:
        res = subprocess.run(
            cmd,
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
def compile_logo_catalog(profile_name: str) -> str:
    """
    Compile generated brand logos from state.json into an interactive HTML catalog page.
    
    Args:
        profile_name: The name of the business profile.
    """
    script_path = os.path.join(os.path.dirname(__file__), "grill-logo", "logo_parser.py")
    try:
        res = subprocess.run(
            [sys.executable, script_path, profile_name],
            capture_output=True, text=True, check=True
        )
        return res.stdout
    except Exception as e:
        return f"Error compiling logo catalog: {str(e)}"

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
def compile_card_gallery(profile_name: str) -> str:
    """
    Generate the style gallery HTML page for a business card profile.
    Uses state.json card_styles if present; falls back to built-in defaults.

    Args:
        profile_name: The profile name (maps to grillbiz-profiles/cards/{profile_name}/state.json).
    """
    script_path = os.path.join(os.path.dirname(__file__), "grill-card", "card_parser.py")
    try:
        res = subprocess.run(
            [sys.executable, script_path, profile_name, "gallery"],
            capture_output=True, text=True, check=True
        )
        return res.stdout
    except subprocess.CalledProcessError as e:
        return f"Error compiling card gallery: {e.stderr}"

@mcp.tool()
def compile_card_matrix(profile_name: str) -> str:
    """
    Generate the final team × liked-styles card matrix HTML page for a business card profile.

    Args:
        profile_name: The profile name (maps to grillbiz-profiles/cards/{profile_name}/state.json).
    """
    script_path = os.path.join(os.path.dirname(__file__), "grill-card", "card_parser.py")
    try:
        res = subprocess.run(
            [sys.executable, script_path, profile_name, "cards"],
            capture_output=True, text=True, check=True
        )
        return res.stdout
    except subprocess.CalledProcessError as e:
        return f"Error compiling card matrix: {e.stderr}"

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

def _get_profile_manager():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "profile_manager", 
        os.path.join(os.path.dirname(__file__), "grill-biz", "profile_manager.py")
    )
    profile_manager = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(profile_manager)
    return profile_manager


@mcp.tool()
def list_business_profiles() -> str:
    """
    List all active business profiles currently stored in the workspace.
    """
    try:
        pm = _get_profile_manager()
        profiles = pm.list_profiles()
        return json.dumps(profiles)
    except Exception as e:
        return f"Error listing profiles: {str(e)}"

@mcp.tool()
def select_business_profile(profile_name: str = None) -> str:
    """
    Check and select the active business profile name. If omitted and ambiguous, returns list of options.
    
    Args:
        profile_name: (Optional) The specific business profile name.
    """
    try:
        pm = _get_profile_manager()
        selected = pm.select_profile(profile_name)
        if selected:
            return json.dumps({"status": "selected", "profile": selected})
        else:
            return json.dumps({"status": "ambiguous", "profiles": pm.list_profiles()})
    except Exception as e:
        return f"Error selecting profile: {str(e)}"



@mcp.tool()
def remove_image_background(input_path: str, output_path: str = "") -> str:
    """
    Remove the background from a logo or photo image using the rembg AI model.
    Outputs a transparent RGBA PNG. Auto-installs rembg if not present.

    Args:
        input_path: Absolute or workspace-relative path to the source image (PNG, JPG, WEBP).
        output_path: (Optional) Where to save the result. Defaults to same path with '_nobg.png' suffix.
    """
    script_path = os.path.join(os.path.dirname(__file__), "grill-background", "remove_bg.py")
    cmd = [sys.executable, script_path, input_path]
    if output_path:
        cmd.append(output_path)
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout
    except subprocess.CalledProcessError as e:
        return f"Error removing background: {e.stderr or e.stdout}"


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
def grill_logo_workflow() -> str:
    """Load the Grill-Logo brand logo creation, selection, and refinement guidelines."""
    return _read_skill_instructions("grill-logo")

@mcp.prompt()
def grill_card_workflow() -> str:
    """Load the Grill-Card business card generation stepper instructions."""
    return _read_skill_instructions("grill-card")

@mcp.prompt()
def grill_bio_workflow() -> str:
    """Load the Grill-Bio mobile bio link website builder and deployment workflow."""
    return _read_skill_instructions("grill-bio")

@mcp.prompt()
def grill_home_workflow() -> str:
    """Load the Grill-Home strategic business homepage stepper and layout configuration guidelines."""
    return _read_skill_instructions("grill-home")

@mcp.prompt()
def grill_background_workflow() -> str:
    """Load the Grill-Background image background removal skill instructions."""
    return _read_skill_instructions("grill-background")

@mcp.prompt()
def grill_post_workflow() -> str:
    """Load the Grill-Post social media draft and automated API publishing workflow."""
    return _read_skill_instructions("grill-post")


if __name__ == "__main__":
    mcp.run()
