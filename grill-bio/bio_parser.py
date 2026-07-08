#!/usr/bin/env python3
import os
import sys
import json
import importlib.util

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

# Import profile_manager dynamically
spec = importlib.util.spec_from_file_location(
    "profile_manager", 
    os.path.join(WORKSPACE_DIR, "grill-biz", "profile_manager.py")
)
profile_manager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(profile_manager)

def _resolve_logo_path(profile_name: str, logo_url: str) -> str:
    if not logo_url:
        return None
    if os.path.isabs(logo_url):
        return logo_url if os.path.exists(logo_url) else None
    candidate = os.path.normpath(
        os.path.join(WORKSPACE_DIR, "grillbiz-profiles", profile_name, logo_url)
    )
    return candidate if os.path.exists(candidate) else None

def ensure_logo_no_bg(profile_name: str, logo_url: str, force_remove: bool = False) -> str:
    if not force_remove:
        return logo_url
        
    abs_path = _resolve_logo_path(profile_name, logo_url)
    if not abs_path:
        return logo_url

    base, _ = os.path.splitext(abs_path)
    nobg_path = f"{base}_nobg.png"

    if os.path.exists(nobg_path):
        return logo_url.replace(os.path.basename(logo_url), os.path.basename(nobg_path))

    try:
        from PIL import Image
        img = Image.open(abs_path).convert("RGBA")
        alpha = img.split()[3]
        min_alpha = alpha.getextrema()[0]
        has_transparency = min_alpha < 250
    except Exception:
        return logo_url

    if has_transparency:
        return logo_url

    print(f"  [logo] Solid background detected and removal is requested. Running grill-background…")
    remove_bg_script = os.path.join(WORKSPACE_DIR, "grill-background", "remove_bg.py")
    try:
        import subprocess
        result = subprocess.run(
            [sys.executable, remove_bg_script, abs_path, nobg_path],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0 and os.path.exists(nobg_path):
            print(f"  [logo] Background removed ✅ → {os.path.basename(nobg_path)}")
            return logo_url.replace(os.path.basename(logo_url), os.path.basename(nobg_path))
    except Exception:
        pass
    return logo_url


# 5 Curated presets aligned with UI Pro Max database style options
DEFAULT_BIO_STYLES = [
    {
        "id": "glassmorphism",
        "name": "Glassmorphism Tech",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');",
        "font_headers": "'Outfit', sans-serif",
        "font_body": "'Outfit', sans-serif",
        "body_bg": "radial-gradient(circle at top, #141822 0%, #0d0f14 100%)",
        "text_primary": "#f1f3f9",
        "text_muted": "#8f9cae",
        "card_bg": "rgba(20, 24, 33, 0.65)",
        "card_border": "1px solid rgba(0, 210, 255, 0.15)",
        "card_shadow": "0 10px 30px rgba(0, 0, 0, 0.4)",
        "card_blur": "blur(12px)",
        "avatar_border": "2px solid rgba(0, 210, 255, 0.3)",
        "avatar_radius": "50%",
        "social_bg": "rgba(255, 255, 255, 0.03)",
        "social_border": "1px solid rgba(255, 255, 255, 0.08)",
        "social_hover_bg": "rgba(0, 210, 255, 0.08)",
        "button_bg": "rgba(20, 24, 33, 0.5)",
        "button_border": "1px solid rgba(0, 210, 255, 0.12)",
        "button_color": "#00d2ff",
        "button_radius": "30px",
        "button_shadow": "none",
        "button_hover_bg": "#00d2ff",
        "button_hover_color": "#0d0f14",
        "button_hover_border": "#00d2ff",
        "item_bg": "rgba(255, 255, 255, 0.02)",
        "item_border": "1px solid rgba(255, 255, 255, 0.05)",
        "item_radius": "12px",
        "item_shadow": "none",
        "item_hover_shadow": "0 8px 25px rgba(0, 210, 255, 0.15)",
        "accent_color": "#00d2ff",
        "price_color": "#ff7b00",
        "divider_style": "1px solid rgba(255, 255, 255, 0.08)",
        "layout": "hub"
    },
    {
        "id": "dark_minimalist",
        "name": "Flat Minimal Dark",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');",
        "font_headers": "'Space Grotesk', sans-serif",
        "font_body": "'Space Grotesk', sans-serif",
        "body_bg": "#050505",
        "text_primary": "#ffffff",
        "text_muted": "#888888",
        "card_bg": "#0a0a0a",
        "card_border": "1px solid #1c1c1c",
        "card_shadow": "0 4px 20px rgba(0,0,0,0.8)",
        "card_blur": "none",
        "avatar_border": "2px solid #333333",
        "avatar_radius": "16px",
        "social_bg": "#111111",
        "social_border": "1px solid #222222",
        "social_hover_bg": "#ffffff",
        "button_bg": "#0f0f0f",
        "button_border": "1px solid #222222",
        "button_color": "#ffffff",
        "button_radius": "8px",
        "button_shadow": "none",
        "button_hover_bg": "#ffffff",
        "button_hover_color": "#050505",
        "button_hover_border": "#ffffff",
        "item_bg": "#0a0a0a",
        "item_border": "1px solid #1c1c1c",
        "item_radius": "8px",
        "item_shadow": "none",
        "item_hover_shadow": "0 4px 15px rgba(255,255,255,0.05)",
        "accent_color": "#ffffff",
        "price_color": "#ffffff",
        "divider_style": "1px solid #1a1a1a",
        "layout": "hub"
    },
    {
        "id": "organic_biophilic",
        "name": "Organic Wellness Sage",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=Montserrat:wght@400;500;600&display=swap');",
        "font_headers": "'Lora', serif",
        "font_body": "'Montserrat', sans-serif",
        "body_bg": "#f4f7f5",
        "text_primary": "#2d3830",
        "text_muted": "#687a6c",
        "card_bg": "#ffffff",
        "card_border": "1px solid #e1e7e3",
        "card_shadow": "0 8px 24px rgba(45, 56, 48, 0.04)",
        "card_blur": "none",
        "avatar_border": "2px solid #a8c3b1",
        "avatar_radius": "50%",
        "social_bg": "#f4f7f5",
        "social_border": "1px solid #e1e7e3",
        "social_hover_bg": "#a8c3b1",
        "button_bg": "#ffffff",
        "button_border": "1px solid #a8c3b1",
        "button_color": "#2d3830",
        "button_radius": "24px",
        "button_shadow": "none",
        "button_hover_bg": "#2d3830",
        "button_hover_color": "#ffffff",
        "button_hover_border": "#2d3830",
        "item_bg": "#ffffff",
        "item_border": "1px solid #e1e7e3",
        "item_radius": "16px",
        "item_shadow": "none",
        "item_hover_shadow": "0 8px 20px rgba(45, 56, 48, 0.08)",
        "accent_color": "#4a6b53",
        "price_color": "#8ea693",
        "divider_style": "1px solid #e1e7e3",
        "layout": "hub"
    },
    {
        "id": "gradient_bold",
        "name": "Neon Pop Vibrant",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');",
        "font_headers": "'Outfit', sans-serif",
        "font_body": "'Outfit', sans-serif",
        "body_bg": "linear-gradient(135deg, #120326 0%, #060112 100%)",
        "text_primary": "#ffffff",
        "text_muted": "#aa9bc5",
        "card_bg": "rgba(27, 10, 58, 0.6)",
        "card_border": "1px solid rgba(255, 0, 128, 0.2)",
        "card_shadow": "0 10px 40px rgba(255, 0, 128, 0.15)",
        "card_blur": "blur(10px)",
        "avatar_border": "2.5px solid #ff007b",
        "avatar_radius": "50%",
        "social_bg": "rgba(255, 255, 255, 0.02)",
        "social_border": "1px solid rgba(255, 255, 255, 0.06)",
        "social_hover_bg": "linear-gradient(90deg, #ff007b, #7b00ff)",
        "button_bg": "linear-gradient(90deg, rgba(255, 0, 128, 0.1), rgba(123, 0, 255, 0.1))",
        "button_border": "1px solid rgba(255, 0, 128, 0.3)",
        "button_color": "#ff007b",
        "button_radius": "30px",
        "button_shadow": "0 4px 15px rgba(255, 0, 128, 0.1)",
        "button_hover_bg": "linear-gradient(90deg, #ff007b, #7b00ff)",
        "button_hover_color": "#ffffff",
        "button_hover_border": "transparent",
        "item_bg": "rgba(27, 10, 58, 0.4)",
        "item_border": "1px solid rgba(255, 0, 128, 0.15)",
        "item_radius": "14px",
        "item_shadow": "none",
        "item_hover_shadow": "0 8px 25px rgba(255, 0, 128, 0.25)",
        "accent_color": "#ff007b",
        "price_color": "#00f0ff",
        "divider_style": "1px solid rgba(255, 255, 255, 0.05)",
        "layout": "hub"
    },
    {
        "id": "classic_light",
        "name": "Elegant Soft Light",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,700;1,400&family=Montserrat:wght@400;500;600&display=swap');",
        "font_headers": "'Cormorant Garamond', serif",
        "font_body": "'Montserrat', sans-serif",
        "body_bg": "#fafafa",
        "text_primary": "#1b202c",
        "text_muted": "#6b7280",
        "card_bg": "#ffffff",
        "card_border": "1px solid #eaeaea",
        "card_shadow": "0 8px 30px rgba(0,0,0,0.03)",
        "card_blur": "none",
        "avatar_border": "2px solid #1b202c",
        "avatar_radius": "50%",
        "social_bg": "#fafafa",
        "social_border": "1px solid #eaeaea",
        "social_hover_bg": "#1b202c",
        "button_bg": "#ffffff",
        "button_border": "1px solid #1b202c",
        "button_color": "#1b202c",
        "button_radius": "0px",
        "button_shadow": "none",
        "button_hover_bg": "#1b202c",
        "button_hover_color": "#ffffff",
        "button_hover_border": "#1b202c",
        "item_bg": "#ffffff",
        "item_border": "1px solid #eaeaea",
        "item_radius": "0px",
        "item_shadow": "none",
        "item_hover_shadow": "0 10px 20px rgba(0,0,0,0.05)",
        "accent_color": "#1b202c",
        "price_color": "#b8860b",
        "divider_style": "1px solid #eaeaea",
        "layout": "classic"
    }
]

def _build_style_css(style: dict, selector_prefix: str = "") -> str:
    """Generate CSS variable declarations based on a BioStyle JSON object."""
    p = selector_prefix + " " if selector_prefix else ""
    return f"""
{p}{{
  --font-headers: {style.get('font_headers', "'Outfit', sans-serif")};
  --font-body: {style.get('font_body', "'Outfit', sans-serif")};
  --body-bg: {style.get('body_bg', '#0b0c10')};
  --text-primary: {style.get('text_primary', '#f1f3f9')};
  --text-muted: {style.get('text_muted', '#9ba3b2')};
  --card-bg: {style.get('card_bg', 'rgba(20, 24, 33, 0.7)')};
  --card-border: {style.get('card_border', '1px solid rgba(255, 255, 255, 0.08)')};
  --card-shadow: {style.get('card_shadow', 'none')};
  --card-blur: {style.get('card_blur', 'blur(15px)')};
  --avatar-border: {style.get('avatar_border', '2px solid rgba(0, 210, 255, 0.3)')};
  --avatar-radius: {style.get('avatar_radius', '50%')};
  --social-bg: {style.get('social_bg', 'rgba(255, 255, 255, 0.04)')};
  --social-border: {style.get('social_border', '1px solid rgba(255, 255, 255, 0.08)')};
  --social-hover-bg: {style.get('social_hover_bg', 'rgba(0, 210, 255, 0.08)')};
  --button-radius: {style.get('button_radius', '30px')};
  --button-bg: {style.get('button_bg', 'rgba(255, 255, 255, 0.03)')};
  --button-border: {style.get('button_border', '1px solid rgba(255, 255, 255, 0.05)')};
  --button-color: {style.get('button_color', '#f1f3f9')};
  --button-shadow: {style.get('button_shadow', 'none')};
  --button-hover-bg: {style.get('button_hover_bg', '#f1f3f9')};
  --button-hover-color: {style.get('button_hover_color', '#0b0c10')};
  --button-hover-border: {style.get('button_hover_border', '#f1f3f9')};
  --item-bg: {style.get('item_bg', 'rgba(255, 255, 255, 0.02)')};
  --item-border: {style.get('item_border', '1px solid rgba(255, 255, 255, 0.05)')};
  --item-radius: {style.get('item_radius', '12px')};
  --item-shadow: {style.get('item_shadow', 'none')};
  --item-hover-shadow: {style.get('item_hover_shadow', 'none')};
  --accent-color: {style.get('accent_color', '#00d2ff')};
  --price-color: {style.get('price_color', '#ff7b00')};
  --divider-style: {style.get('divider_style', '1px solid rgba(255, 255, 255, 0.05)')};
}}
"""

def generate_gallery(profile_name: str):
    """Generates the Bio website style selection gallery page."""
    state = profile_manager.load_profile_state(profile_name)
    company = state.get("company", profile_name.upper())
    logo_url = state.get("logo_url", "")
    force_remove = state.get("remove_logo_background", False)
    logo_url = ensure_logo_no_bg(profile_name, logo_url, force_remove=force_remove)
    
    # Prefix logo with relative parent if running from subfolder
    html_logo_url = f"../{logo_url}" if logo_url and not logo_url.startswith("http") else logo_url
    tagline = state.get("tagline", "")
    round_num = state.get("round", 1)
    
    # Get content lists
    socials = state.get("socials", []) or [{"platform": "Instagram", "url": "#"}, {"platform": "Patreon", "url": "#"}, {"platform": "GitHub", "url": "#"}]
    pills = state.get("links", []) or [{"title": "Visit Our Shop", "url": "#"}, {"title": "Join Newsletter", "url": "#"}]
    products = state.get("products", [])
    blogs = state.get("blogs", [])
    
    # Fallback product for visual mockup preview
    if not products and not blogs:
        products = [
            {"title": "Mindful Tea Blend", "description": "Soothing organic loose-leaf tea.", "price": "$18", "url": "#", "image_url": "https://cdn-icons-png.flaticon.com/512/3649/3649775.png"},
            {"title": "Ceremony Bowl", "description": "Handcrafted matcha clay bowl.", "price": "$45", "url": "#", "image_url": "https://cdn-icons-png.flaticon.com/512/3135/3135679.png"}
        ]
        
    bio_styles = state.get("bio_styles") or DEFAULT_BIO_STYLES
    
    # 1. Compile Google Fonts imports and theme CSS
    font_imports = []
    dynamic_css = ""
    for style in bio_styles:
        sid = style["id"]
        if style.get("font_import") and style["font_import"] not in font_imports:
            font_imports.append(style["font_import"])
            
        # Scope variables to .phone-frame.s-{id}
        prefix = f".phone-frame.s-{sid}"
        dynamic_css += _build_style_css(style, prefix)
        
    font_imports_html = "\n    ".join(font_imports)
    
    # 2. Build mock HTML items
    social_pills_html = ""
    for s in socials:
        social_pills_html += f'<a class="p-social-btn" href="#">{s["platform"]}</a>\n'
        
    pill_buttons_html = ""
    for p in pills:
        pill_buttons_html += f'<a class="p-pill-btn" href="#"><span>{p["title"]}</span><span>→</span></a>\n'
        
    feed_grid_html = ""
    for item in products[:2]:
        feed_grid_html += f"""
        <div class="f-item">
            <img class="f-img" src="{item.get('image_url', '')}">
            <div class="f-details">
                <span class="f-title">{item.get('title', '')}</span>
                <span class="f-price">{item.get('price', '')}</span>
            </div>
        </div>"""
        
    # 3. Build style card HTML blocks
    styles_html = ""
    liked = set(state.get("liked_bio_styles", []))
    for style in bio_styles:
        sid = style["id"]
        is_liked = sid in liked
        selected_class = "selected" if is_liked else ""
        btn_class = "active" if is_liked else ""
        btn_label = "<span>❤️</span> Selected" if is_liked else "<span>🤍</span> Select Style"
        layout_class = f"layout-{style.get('layout', 'hub')}"
        
        styles_html += f"""
    <div class="style-card {selected_class}" id="style-card-{sid}">
        <div class="style-card-header">
            <span class="style-name">{style['name']}</span>
            <span class="style-round">Round {round_num}</span>
        </div>
        <div class="mockup-viewport">
            <div class="phone-frame s-{sid} {layout_class}">
                <div class="p-card">
                    <div class="p-avatar">
                        <img src="{html_logo_url}" alt="logo" onerror="this.src='https://cdn-icons-png.flaticon.com/512/3135/3135715.png';">
                    </div>
                    <div class="p-title">{company}</div>
                    <div class="p-tagline">{tagline or 'Describe your business tagline here...'}</div>
                    <div class="p-social-row">
                        {social_pills_html}
                    </div>
                </div>
                
                <div class="p-pills-container">
                    {pill_buttons_html}
                </div>
                
                <div class="sect-title">Latest Shop & Posts</div>
                <div class="f-grid">
                    {feed_grid_html}
                </div>
            </div>
        </div>
        <div class="style-card-footer">
            <button id="select-btn-{sid}" class="select-btn {btn_class}" onclick="toggleStyle('{sid}')">
                {btn_label}
            </button>
        </div>
    </div>"""

    # 4. Load gallery template and render
    gallery_template = os.path.join(TEMPLATES_DIR, "bio_gallery.html")
    with open(gallery_template, "r", encoding="utf-8") as f:
        template = f.read()
        
    rendered = template
    rendered = rendered.replace("{{COMPANY}}", company)
    rendered = rendered.replace("{{ROUND}}", str(round_num))
    rendered = rendered.replace("{{FONT_IMPORTS}}", font_imports_html)
    rendered = rendered.replace("{{STYLES_HTML}}", styles_html)
    rendered = rendered.replace("{{DYNAMIC_STYLE_CSS}}", dynamic_css)
    
    # Save output to grillbiz-profiles/{profile_name}/bio/{profile_name}_bio_gallery.html
    out_dir = os.path.join(WORKSPACE_DIR, "grillbiz-profiles", profile_name, "bio")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{profile_name}_style_gallery.html")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)
        
    print(f"Success: Generated bio style gallery at {out_path}")

def generate_bio_page(profile_name: str):
    """Generates the final bio landing website with the selected style."""
    state = profile_manager.load_profile_state(profile_name)
    company = state.get("company", profile_name.upper())
    logo_url = state.get("logo_url", "")
    force_remove = state.get("remove_logo_background", False)
    logo_url = ensure_logo_no_bg(profile_name, logo_url, force_remove=force_remove)
    
    html_logo_url = f"../{logo_url}" if logo_url and not logo_url.startswith("http") else logo_url
    tagline = state.get("tagline", "")
    
    # Get active/selected style
    liked_styles = state.get("liked_bio_styles", [])
    all_styles = state.get("bio_styles") or DEFAULT_BIO_STYLES
    
    selected_style = None
    if liked_styles:
        # Match the first liked style
        style_map = {s["id"]: s for s in all_styles}
        selected_style = style_map.get(liked_styles[0])
        
    if not selected_style:
        # Fallback to the first style
        selected_style = all_styles[0]
        
    # CSS Override
    font_imports_html = selected_style.get("font_import", "")
    scoped_css = _build_style_css(selected_style, "body")
    layout_name = selected_style.get("layout", "hub")
    
    # Content JSON Strings
    socials_json = json.dumps(state.get("socials", []))
    links_json = json.dumps(state.get("links", []))
    products_json = json.dumps(state.get("products", []))
    blogs_json = json.dumps(state.get("blogs", []))
    
    # Load bio template
    bio_template = os.path.join(TEMPLATES_DIR, "bio_template.html")
    with open(bio_template, "r", encoding="utf-8") as f:
        template = f.read()
        
    rendered = template
    rendered = rendered.replace("{{COMPANY}}", company)
    rendered = rendered.replace("{{BIO_DESCRIPTION}}", tagline)
    rendered = rendered.replace("{{LOGO_URL}}", html_logo_url)
    rendered = rendered.replace("{{FONT_IMPORTS}}", font_imports_html)
    rendered = rendered.replace("{{DYNAMIC_STYLE_CSS}}", scoped_css)
    
    rendered = rendered.replace("{{SOCIAL_DATA_JSON}}", socials_json)
    rendered = rendered.replace("{{LINKS_DATA_JSON}}", links_json)
    rendered = rendered.replace("{{PRODUCTS_DATA_JSON}}", products_json)
    rendered = rendered.replace("{{BLOGS_DATA_JSON}}", blogs_json)
    
    # Replace body class layout
    rendered = rendered.replace('<body class="layout-hub">', f'<body class="layout-{layout_name}">')
    
    # Save output to grillbiz-profiles/{profile_name}/bio/{profile_name}_bio.html
    out_dir = os.path.join(WORKSPACE_DIR, "grillbiz-profiles", profile_name, "bio")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{profile_name}_bio.html")
    
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)
        
    print(f"Success: Generated final bio link website at {out_path}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 bio_parser.py <profile_name> gallery|bio")
        sys.exit(1)
        
    profile_name = sys.argv[1].strip().lower()
    mode = sys.argv[2].strip().lower()
    
    if mode == "gallery":
        generate_gallery(profile_name)
    elif mode == "bio":
        generate_bio_page(profile_name)
    else:
        print(f"Error: Unknown mode '{mode}'. Use 'gallery' or 'bio'.")
        sys.exit(1)

if __name__ == "__main__":
    main()
