#!/usr/bin/env python3
"""
Grill-Card Card Parser
Usage:
    python3 grill-card/card_parser.py <profile_name> gallery   # generate style gallery
    python3 grill-card/card_parser.py <profile_name> cards     # generate final card matrix

CardStyle JSON schema (stored in state.json under "card_styles"):
[
  {
    "id": "style_1",
    "name": "Human-readable style name",
    "card_bg": "CSS background value (color, gradient, or url)",
    "card_border": "CSS border value e.g. '2px solid rgba(0,210,255,0.3)'",
    "card_shadow": "CSS box-shadow value",
    "card_border_radius": "CSS border-radius e.g. '20px'",
    "accent_line": "CSS background for optional top stripe e.g. 'linear-gradient(90deg,#f00,#0f0)' or ''",
    "glow_before": "CSS radial-gradient for ::before glow blob or ''",
    "glow_after": "CSS radial-gradient for ::after glow blob or ''",
    "text_primary": "CSS color for company name / back name",
    "text_secondary": "CSS color for tagline / role / info values",
    "text_accent": "CSS color for role highlight (used on back)",
    "text_label": "CSS color for info label (small uppercase)",
    "divider_color": "CSS border-left color for back-right panel",
    "logo_blend": "CSS mix-blend-mode for logo img e.g. 'multiply' or 'luminosity' or 'normal'",
    "logo_radius": "CSS border-radius for logo wrapper e.g. '12px' or '50%' or '0'"
  }
]
"""

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


# Fallback styles used when state.json has no card_styles defined
DEFAULT_CARD_STYLES = [
    {
        "id": "wellness_neumorphic",
        "name": "Soft Wellness Sage",
        "layout": "classic",
        "card_bg": "#faf9f6",
        "card_border": "1px solid rgba(220, 225, 220, 0.6)",
        "card_shadow": "-4px -4px 12px rgba(255,255,255,0.9), 4px 4px 12px rgba(180,190,180,0.2)",
        "card_border_radius": "0px",
        "font_headers": "'Lora', serif",
        "font_body": "'Raleway', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Lora:wght@500;700&family=Raleway:wght@400;500;600&display=swap');",
        "text_primary": "#1c2b24",
        "text_secondary": "#556f60",
        "text_accent": "#059669",
        "text_label": "rgba(28, 43, 36, 0.4)",
        "divider_color": "rgba(220, 225, 220, 0.8)",
        "logo_blend": "normal",
        "logo_radius": "12px",
        "front_html": """
        <div class="card-front layout-wellness">
            <div class="organic-leaf-bg"></div>
            <div class="card-logo-circle">
                <img src="{{LOGO_URL}}" alt="{{COMPANY}} logo"
                     onerror="this.style.display='none';document.getElementById('{{LOGO_FALLBACK_ID}}').style.display='block';">
                <div class="fallback-txt" id="{{LOGO_FALLBACK_ID}}" style="display:none;">{{COMPANY}}</div>
            </div>
            <div class="brand-text">
                <h1 class="comp-title">{{COMPANY}}</h1>
                {{TAGLINE}}
            </div>
        </div>
        """,
        "back_html": """
        <div class="card-back layout-wellness-back">
            <div class="back-left">
                <div class="back-name">{{NAME}}</div>
                <div class="back-role">{{ROLE}}</div>
                <div class="back-company-tag">{{COMPANY}}</div>
            </div>
            <div class="back-right">{{INFO_ROWS}}</div>
        </div>
        """,
        "custom_css": """
        {{P}} .card-front.layout-wellness {
            display: flex; flex-direction: column; align-items: center; justify-content: center;
            padding: 60px; text-align: center; height: 100%; width: 100%; position: relative;
        }
        {{P}} .organic-leaf-bg {
            position: absolute; top: -100px; right: -100px; width: 300px; height: 300px;
            background: radial-gradient(circle, rgba(5,150,105,0.06) 0%, transparent 70%);
            border-radius: 50%; pointer-events: none;
        }
        {{P}} .card-logo-circle {
            width: 140px; height: 140px; border-radius: 50%; background: #ffffff;
            box-shadow: inset 2px 2px 5px rgba(0,0,0,0.03), 4px 4px 10px rgba(5,150,105,0.06);
            display: flex; align-items: center; justify-content: center; padding: 25px; margin-bottom: 15px;
        }
        {{P}} .card-logo-circle img { max-height: 90px; max-width: 90px; object-fit: contain; }
        {{P}} .comp-title { font-size: 2.8rem; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
        {{P}} .card-front.layout-wellness .card-tagline { font-size: 1.1rem; font-weight: 500; opacity: 0.6; margin-top: 5px; }
        {{P}} .card-back.layout-wellness-back {
            display: flex; align-items: center; justify-content: space-between;
            padding: 60px; gap: 40px; width: 100%; height: 100%;
        }
        """
    },
    {
        "id": "asymmetric_zen",
        "name": "Asymmetric Zen Offset",
        "layout": "asymmetric",
        "card_bg": "#ffffff",
        "card_border": "1px solid rgba(28, 60, 58, 0.1)",
        "card_shadow": "0 10px 30px rgba(0,0,0,0.02)",
        "card_border_radius": "0px",
        "font_headers": "'Cormorant Garamond', serif",
        "font_body": "'Montserrat', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,700;1,400&family=Montserrat:wght@400;500;600&display=swap');",
        "text_primary": "#1c3c3a",
        "text_secondary": "#5c6d6a",
        "text_accent": "#0d9488",
        "text_label": "rgba(28, 60, 58, 0.35)",
        "divider_color": "rgba(28, 60, 58, 0.12)",
        "logo_blend": "normal",
        "logo_radius": "4px",
        "front_html": """,
        <div class="card-front layout-asymmetric-zen">
            <div class="logo-box">
                <img src="{{LOGO_URL}}" alt="{{COMPANY}} logo"
                     onerror="this.style.display='none';document.getElementById('{{LOGO_FALLBACK_ID}}').style.display='block';">
                <div class="fallback-txt" id="{{LOGO_FALLBACK_ID}}" style="display:none;">{{COMPANY}}</div>
            </div>
            <div class="text-box">
                <div class="line-accent"></div>
                <h1 class="comp-title">{{COMPANY}}</h1>
                {{TAGLINE}}
            </div>
        </div>
        """,
        "back_html": """
        <div class="card-back layout-asymmetric-zen-back">
            <div class="back-left">{{INFO_ROWS}}</div>
            <div class="back-right">
                <div class="back-name">{{NAME}}</div>
                <div class="back-role">{{ROLE}}</div>
                <div class="back-company-tag">{{COMPANY}}</div>
            </div>
        </div>
        """,
        "custom_css": """
        {{P}} .card-front.layout-asymmetric-zen {
            display: flex; flex-direction: row; align-items: center; justify-content: space-between;
            padding: 80px; height: 100%; width: 100%; position: relative;
        }
        {{P}} .logo-box {
            width: 180px; height: 180px; display: flex; align-items: center; justify-content: center;
        }
        {{P}} .logo-box img { max-height: 150px; max-width: 180px; object-fit: contain; }
        {{P}} .text-box {
            text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 8px;
        }
        {{P}} .text-box .line-accent {
            width: 80px; height: 3px; background: #0d9488; margin-bottom: 8px;
        }
        {{P}} .text-box .comp-title { font-size: 3.2rem; font-weight: 600; margin: 0; }
        {{P}} .card-front.layout-asymmetric-zen .card-tagline { font-size: 1.1rem; opacity: 0.55; margin: 0; }
        {{P}} .card-back.layout-asymmetric-zen-back {
            display: flex; align-items: center; justify-content: space-between;
            padding: 60px; gap: 40px; width: 100%; height: 100%; flex-direction: row-reverse;
        }
        {{P}} .card-back.layout-asymmetric-zen-back .back-right {
            text-align: left; align-items: flex-start; border-left: none; padding-left: 0;
        }
        {{P}} .card-back.layout-asymmetric-zen-back .back-left {
            align-items: flex-end;
        }
        """
    },
    {
        "id": "vertical_bamboo",
        "name": "Vertical Bamboo Split",
        "layout": "vertical",
        "card_bg": "#ffffff",
        "card_border": "1px solid rgba(0,0,0,0.06)",
        "card_shadow": "0 8px 24px rgba(0,0,0,0.03)",
        "card_border_radius": "0px",
        "font_headers": "'Playfair Display', serif",
        "font_body": "'Inter', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Inter:wght@400;500;600&display=swap');",
        "text_primary": "#111827",
        "text_secondary": "#4b5563",
        "text_accent": "#059669",
        "text_label": "rgba(17, 24, 39, 0.35)",
        "divider_color": "rgba(17, 24, 39, 0.08)",
        "logo_blend": "normal",
        "logo_radius": "50%",
        "front_html": """
        <div class="card-front layout-vertical-bamboo">
            <div class="left-sidebar">
                <div class="rotated-name">{{COMPANY}}</div>
            </div>
            <div class="right-main">
                <div class="logo-circle">
                    <img src="{{LOGO_URL}}" alt="{{COMPANY}} logo"
                         onerror="this.style.display='none';document.getElementById('{{LOGO_FALLBACK_ID}}').style.display='block';">
                    <div class="fallback-txt" id="{{LOGO_FALLBACK_ID}}" style="display:none;">{{COMPANY}}</div>
                </div>
                {{TAGLINE}}
            </div>
        </div>
        """,
        "back_html": """
        <div class="card-back layout-vertical-bamboo-back">
            <div class="back-left">
                <div class="back-name">{{NAME}}</div>
                <div class="back-role">{{ROLE}}</div>
                <div class="back-company-tag">{{COMPANY}}</div>
            </div>
            <div class="back-right">{{INFO_ROWS}}</div>
        </div>
        """,
        "custom_css": """
        {{P}} .card-front.layout-vertical-bamboo {
            display: flex; flex-direction: row; height: 100%; width: 100%; padding: 0; align-items: stretch;
        }
        {{P}} .left-sidebar {
            width: 200px; background: #059669; display: flex; align-items: center; justify-content: center;
        }
        {{P}} .rotated-name {
            writing-mode: vertical-rl; transform: rotate(180deg); font-family: 'Playfair Display', serif;
            font-size: 2.2rem; font-weight: 700; color: #ffffff; letter-spacing: 2px; text-transform: uppercase;
        }
        {{P}} .right-main {
            flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px;
        }
        {{P}} .logo-circle {
            width: 160px; height: 160px; border-radius: 50%; background: #fafafa;
            display: flex; align-items: center; justify-content: center; padding: 25px; margin-bottom: 20px;
            border: 1px solid rgba(5,150,105,0.1);
        }
        {{P}} .logo-circle img { max-height: 110px; max-width: 110px; object-fit: contain; }
        {{P}} .card-front.layout-vertical-bamboo .card-tagline { font-size: 1.25rem; font-weight: 400; opacity: 0.6; }
        {{P}} .card-back.layout-vertical-bamboo-back {
            display: flex; align-items: center; justify-content: space-between;
            padding: 60px; gap: 40px; width: 100%; height: 100%;
        }
        """
    },
    {
        "id": "editorial_line",
        "name": "Editorial Line Minimalist",
        "layout": "minimal_line",
        "card_bg": "#ffffff",
        "card_border": "1px solid rgba(0,0,0,0.08)",
        "card_shadow": "none",
        "card_border_radius": "0px",
        "font_headers": "'Space Grotesk', sans-serif",
        "font_body": "'Inter', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500&display=swap');",
        "text_primary": "#1c2b24",
        "text_secondary": "#4b5c54",
        "text_accent": "#0d9488",
        "text_label": "rgba(28, 43, 36, 0.35)",
        "divider_color": "rgba(28, 43, 36, 0.1)",
        "logo_blend": "normal",
        "logo_radius": "0px"
    },
    {
        "id": "slate_split",
        "name": "Zen Slate Split-Color",
        "layout": "split_color",
        "card_bg": "#ffffff",
        "card_border": "1px solid rgba(0,0,0,0.06)",
        "card_shadow": "0 8px 30px rgba(0,0,0,0.02)",
        "card_border_radius": "0px",
        "font_headers": "'Outfit', sans-serif",
        "font_body": "'Inter', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;700&family=Inter:wght@400;500&display=swap');",
        "text_primary": "#1e293b",
        "text_secondary": "#64748b",
        "text_accent": "#0f766e",
        "text_label": "rgba(30, 41, 59, 0.35)",
        "divider_color": "rgba(0,0,0,0.06)",
        "logo_blend": "normal",
        "logo_radius": "8px"
    },
    {
        "id": "classic_gold",
        "name": "Classic Luxury Gold",
        "layout": "classic",
        "card_bg": "#ffffff",
        "card_border": "1px solid #c5a880",
        "card_shadow": "0 4px 15px rgba(197, 168, 128, 0.05)",
        "card_border_radius": "0px",
        "font_headers": "'Cormorant Garamond', serif",
        "font_body": "'Montserrat', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,700;1,400&family=Montserrat:wght@400;500;600&display=swap');",
        "text_primary": "#1b202c",
        "text_secondary": "#5c6270",
        "text_accent": "#c5a880",
        "text_label": "rgba(27, 32, 44, 0.4)",
        "divider_color": "#e2d5c3",
        "logo_blend": "normal",
        "logo_radius": "0px",
        "front_html": """
        <div class="card-front layout-classic-gold">
            <div class="gold-border-inset">
                <div class="logo-container">
                    <img src="{{LOGO_URL}}" alt="{{COMPANY}} logo"
                         onerror="this.style.display='none';document.getElementById('{{LOGO_FALLBACK_ID}}').style.display='block';">
                    <div class="fallback-txt" id="{{LOGO_FALLBACK_ID}}" style="display:none;">{{COMPANY}}</div>
                </div>
                <h1 class="comp-title">{{COMPANY}}</h1>
                <div class="gold-bar"></div>
                {{TAGLINE}}
            </div>
        </div>
        """,
        "back_html": """
        <div class="card-back layout-classic-gold-back">
            <div class="gold-border-inset">
                <div class="back-left">
                    <div class="back-name">{{NAME}}</div>
                    <div class="back-role">{{ROLE}}</div>
                    <div class="back-company-tag">{{COMPANY}}</div>
                </div>
                <div class="gold-vertical-divider"></div>
                <div class="back-right">{{INFO_ROWS}}</div>
            </div>
        </div>
        """,
        "custom_css": """
        {{P}} .card-front.layout-classic-gold,
        {{P}} .card-back.layout-classic-gold-back {
            width: 100%; height: 100%; padding: 40px; box-sizing: border-box; display: flex; align-items: stretch; justify-content: stretch;
        }
        {{P}} .gold-border-inset {
            border: 2px solid #c5a880; width: 100%; height: 100%; display: flex;
            flex-direction: column; align-items: center; justify-content: center; padding: 40px; box-sizing: border-box;
            position: relative; flex: 1;
        }
        {{P}} .logo-container {
            width: 180px; height: 110px; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;
        }
        {{P}} .logo-container img { max-height: 100px; max-width: 180px; object-fit: contain; }
        {{P}} .comp-title { font-size: 2.8rem; font-weight: 700; margin: 0; color: #1b202c; text-transform: uppercase; letter-spacing: 1px; }
        {{P}} .gold-bar { width: 120px; height: 2px; background: #c5a880; margin: 15px 0; }
        {{P}} .card-front.layout-classic-gold .card-tagline { font-size: 1.15rem; font-style: italic; opacity: 0.7; margin: 0; }
        {{P}} .card-back.layout-classic-gold-back .gold-border-inset {
            flex-direction: row; align-items: center; justify-content: space-between; padding: 40px;
        }
        {{P}} .card-back.layout-classic-gold-back .gold-vertical-divider {
            width: 2px; height: 100%; background: #e2d5c3; margin: 0 40px;
        }
        {{P}} .card-back.layout-classic-gold-back .back-right {
            border-left: none; padding-left: 0;
        }
        """
    },
    {
        "id": "terrazzo_wellness",
        "name": "Terrazzo Organic Cream",
        "layout": "classic",
        "card_bg": "radial-gradient(circle at 10% 20%, rgba(244,247,245,1) 0%, rgba(250,249,246,1) 100%)",
        "card_border": "1px solid rgba(13,148,136,0.15)",
        "card_shadow": "0 12px 30px rgba(13,148,136,0.03)",
        "card_border_radius": "0px",
        "font_headers": "'Playfair Display', serif",
        "font_body": "'Raleway', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Raleway:wght@400;500&display=swap');",
        "text_primary": "#0f2d29",
        "text_secondary": "#4d6b66",
        "text_accent": "#14b8a6",
        "text_label": "rgba(15,45,41,0.35)",
        "divider_color": "rgba(13,148,136,0.1)",
        "logo_blend": "normal",
        "logo_radius": "50%"
    },
    {
        "id": "minimal_warm",
        "name": "Warm Minimalist Linen",
        "layout": "asymmetric",
        "card_bg": "#faf6f0",
        "card_border": "1px solid rgba(161,114,81,0.15)",
        "card_shadow": "none",
        "card_border_radius": "0px",
        "font_headers": "'Lora', serif",
        "font_body": "'Inter', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,500;0,700;1,400&family=Inter:wght@400;500&display=swap');",
        "text_primary": "#2e251b",
        "text_secondary": "#63584c",
        "text_accent": "#a17251",
        "text_label": "rgba(46,37,27,0.35)",
        "divider_color": "rgba(161,114,81,0.12)",
        "logo_blend": "normal",
        "logo_radius": "6px"
    },
    {
        "id": "japandi_wood",
        "name": "Japandi Oak",
        "layout": "vertical",
        "card_bg": "#fcfbf9",
        "card_border": "1px solid rgba(197,168,128,0.25)",
        "card_shadow": "0 6px 18px rgba(0,0,0,0.01)",
        "card_border_radius": "0px",
        "font_headers": "'Outfit', sans-serif",
        "font_body": "'Inter', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@500;700&family=Inter:wght@400;500&display=swap');",
        "text_primary": "#2d2722",
        "text_secondary": "#5e544d",
        "text_accent": "#b88a5e",
        "text_label": "rgba(45,39,34,0.35)",
        "divider_color": "rgba(197,168,128,0.15)",
        "logo_blend": "normal",
        "logo_radius": "4px"
    },
    {
        "id": "eucalyptus_mist",
        "name": "Eucalyptus Sage",
        "layout": "minimal_line",
        "card_bg": "#f3f6f4",
        "card_border": "1px solid rgba(5,150,105,0.12)",
        "card_shadow": "none",
        "card_border_radius": "0px",
        "font_headers": "'Cormorant Garamond', serif",
        "font_body": "'Raleway', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,700;1,400&family=Raleway:wght@400;500&display=swap');",
        "text_primary": "#1f3328",
        "text_secondary": "#526e5e",
        "text_accent": "#059669",
        "text_label": "rgba(31,51,40,0.35)",
        "divider_color": "rgba(5,150,105,0.15)",
        "logo_blend": "normal",
        "logo_radius": "8px"
    },
    {
        "id": "terracotta_sunset",
        "name": "Terracotta Warmth",
        "layout": "split_color",
        "card_bg": "#fffefe",
        "card_border": "1px solid rgba(220,100,60,0.1)",
        "card_shadow": "0 8px 24px rgba(0,0,0,0.01)",
        "card_border_radius": "0px",
        "font_headers": "'Playfair Display', serif",
        "font_body": "'Montserrat', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Montserrat:wght@400;500&display=swap');",
        "text_primary": "#3a1f16",
        "text_secondary": "#7c5346",
        "text_accent": "#dc643c",
        "text_label": "rgba(58,31,22,0.35)",
        "divider_color": "rgba(220,100,60,0.12)",
        "logo_blend": "normal",
        "logo_radius": "10px"
    },
    {
        "id": "matcha_cream",
        "name": "Matcha Latte Cream",
        "layout": "classic",
        "card_bg": "#f9f8f3",
        "card_border": "1px solid #d4d1bc",
        "card_shadow": "0 4px 12px rgba(212,209,188,0.15)",
        "card_border_radius": "0px",
        "font_headers": "'Lora', serif",
        "font_body": "'Raleway', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Lora:wght@500;700&family=Raleway:wght@400;500&display=swap');",
        "text_primary": "#2b2e1b",
        "text_secondary": "#585d3f",
        "text_accent": "#738b4d",
        "text_label": "rgba(43,46,27,0.35)",
        "divider_color": "rgba(212,209,188,0.4)",
        "logo_blend": "normal",
        "logo_radius": "12px"
    },
    {
        "id": "wabi_sabi_stone",
        "name": "Wabi Sabi Slate",
        "layout": "asymmetric",
        "card_bg": "#eff1f0",
        "card_border": "1px solid #d1d5d4",
        "card_shadow": "none",
        "card_border_radius": "0px",
        "font_headers": "'Cormorant Garamond', serif",
        "font_body": "'Inter', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,700;1,400&family=Inter:wght@400;500&display=swap');",
        "text_primary": "#222c2a",
        "text_secondary": "#556461",
        "text_accent": "#6d7f7c",
        "text_label": "rgba(34,44,42,0.35)",
        "divider_color": "rgba(209,213,212,0.6)",
        "logo_blend": "normal",
        "logo_radius": "0px"
    },
    {
        "id": "botanical_ink",
        "name": "Botanical Charcoal",
        "layout": "vertical",
        "card_bg": "#fafafa",
        "card_border": "1px solid #1c2321",
        "card_shadow": "0 8px 30px rgba(0,0,0,0.02)",
        "card_border_radius": "0px",
        "font_headers": "'DM Serif Display', serif",
        "font_body": "'Montserrat', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Montserrat:wght@400;500;600&display=swap');",
        "text_primary": "#1c2321",
        "text_secondary": "#495854",
        "text_accent": "#0d9488",
        "text_label": "rgba(28,35,33,0.4)",
        "divider_color": "rgba(28,35,33,0.15)",
        "logo_blend": "normal",
        "logo_radius": "10px"
    },
    {
        "id": "breeze_linen",
        "name": "Ocean Breeze Linen",
        "layout": "minimal_line",
        "card_bg": "#f5f8fa",
        "card_border": "1px solid rgba(2,132,199,0.12)",
        "card_shadow": "none",
        "card_border_radius": "0px",
        "font_headers": "'Space Grotesk', sans-serif",
        "font_body": "'Raleway', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Raleway:wght@400;500&display=swap');",
        "text_primary": "#162836",
        "text_secondary": "#455969",
        "text_accent": "#0284c7",
        "text_label": "rgba(22,40,54,0.35)",
        "divider_color": "rgba(2,132,199,0.15)",
        "logo_blend": "normal",
        "logo_radius": "8px"
    },
    {
        "id": "copper_clay",
        "name": "Copper & Clay",
        "layout": "split_color",
        "card_bg": "#fefdfa",
        "card_border": "1px solid rgba(162,94,62,0.15)",
        "card_shadow": "none",
        "card_border_radius": "0px",
        "font_headers": "'Playfair Display', serif",
        "font_body": "'Inter', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;700&family=Inter:wght@400;500&display=swap');",
        "text_primary": "#362016",
        "text_secondary": "#755648",
        "text_accent": "#a25e3e",
        "text_label": "rgba(54,32,22,0.35)",
        "divider_color": "rgba(162,94,62,0.12)",
        "logo_blend": "normal",
        "logo_radius": "8px"
    },
    {
        "id": "yin_yang",
        "name": "Zen Yin Yang",
        "layout": "split_color",
        "card_bg": "#ffffff",
        "card_border": "1px solid #000000",
        "card_shadow": "0 10px 40px rgba(0,0,0,0.05)",
        "card_border_radius": "0px",
        "font_headers": "'Space Grotesk', sans-serif",
        "font_body": "'Inter', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500&display=swap');",
        "text_primary": "#000000",
        "text_secondary": "#555555",
        "text_accent": "#000000",
        "text_label": "rgba(0,0,0,0.4)",
        "divider_color": "#000000",
        "logo_blend": "normal",
        "logo_radius": "0px"
    },
    {
        "id": "lavender_mist",
        "name": "Lavender & Sage Mist",
        "layout": "classic",
        "card_bg": "#f9f8fc",
        "card_border": "1px solid rgba(124,58,237,0.12)",
        "card_shadow": "0 4px 15px rgba(124,58,237,0.03)",
        "card_border_radius": "0px",
        "font_headers": "'Lora', serif",
        "font_body": "'Raleway', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Lora:wght@500;700&family=Raleway:wght@400;500&display=swap');",
        "text_primary": "#2b1c3c",
        "text_secondary": "#63527a",
        "text_accent": "#7c3aed",
        "text_label": "rgba(43,28,60,0.35)",
        "divider_color": "rgba(124,58,237,0.12)",
        "logo_blend": "normal",
        "logo_radius": "12px"
    },
    {
        "id": "imperial_jade",
        "name": "Imperial Jade Gold",
        "layout": "classic",
        "card_bg": "#f4f8f6",
        "card_border": "1px solid #c5a880",
        "card_shadow": "0 8px 24px rgba(28,60,58,0.03)",
        "card_border_radius": "0px",
        "font_headers": "'Cinzel', serif",
        "font_body": "'Montserrat', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;800&family=Montserrat:wght@400;500;600&display=swap');",
        "text_primary": "#0f261c",
        "text_secondary": "#4c6657",
        "text_accent": "#c5a880",
        "text_label": "rgba(15,38,28,0.4)",
        "divider_color": "#e2d5c3",
        "logo_blend": "normal",
        "logo_radius": "4px"
    },
    {
        "id": "silk_road",
        "name": "Silk Road Sand",
        "layout": "asymmetric",
        "card_bg": "#faf7f2",
        "card_border": "1px solid rgba(184,138,94,0.2)",
        "card_shadow": "none",
        "card_border_radius": "0px",
        "font_headers": "'Cormorant Garamond', serif",
        "font_body": "'Raleway', sans-serif",
        "font_import": "@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,700;1,400&family=Raleway:wght@400;500&display=swap');",
        "text_primary": "#3c2818",
        "text_secondary": "#7a5c43",
        "text_accent": "#b88a5e",
        "text_label": "rgba(60,40,24,0.35)",
        "divider_color": "rgba(184,138,94,0.15)",
        "logo_blend": "normal",
        "logo_radius": "0px"
    }
]


def load_state(profile_name: str) -> dict:
    """Load the unified state.json for a given profile."""
    return profile_manager.load_profile_state(profile_name)


def save_state(profile_name: str, state: dict):
    """Save the unified state.json for a profile."""
    profile_manager.save_profile_state(profile_name, state)


def _resolve_logo_path(profile_name: str, logo_url: str) -> str:
    """
    Convert a relative logo_url (e.g. 'logos/logo_1_1.png')
    to an absolute filesystem path.
    Returns None if the file doesn't exist.
    """
    if not logo_url:
        return None
    if os.path.isabs(logo_url):
        return logo_url if os.path.exists(logo_url) else None
    # Relative to unified profile dir
    candidate = os.path.normpath(
        os.path.join(WORKSPACE_DIR, "grillbiz-profiles", profile_name, logo_url)
    )
    if os.path.exists(candidate):
        return candidate
    # Fallback to old path format
    candidate_old = os.path.normpath(
        os.path.join(WORKSPACE_DIR, "grillbiz-profiles", "cards", logo_url)
    )
    return candidate_old if os.path.exists(candidate_old) else None


def ensure_logo_no_bg(profile_name: str, logo_url: str, force_remove: bool = False) -> str:
    """
    Check whether the logo image has a solid/non-transparent background.
    Only run background removal if explicitly forced/requested via force_remove.
    Otherwise, return the original logo_url.
    """
    if not force_remove:
        return logo_url

    abs_path = _resolve_logo_path(profile_name, logo_url)
    if not abs_path:
        return logo_url

    # Derive nobg path
    base, _ = os.path.splitext(abs_path)
    nobg_path = f"{base}_nobg.png"

    if os.path.exists(nobg_path):
        print(f"  [logo] Re-using existing transparent version: {os.path.basename(nobg_path)}")
        return logo_url.replace(os.path.basename(logo_url), os.path.basename(nobg_path))

    try:
        from PIL import Image
    except ImportError:
        return logo_url

    try:
        img = Image.open(abs_path).convert("RGBA")
        alpha = img.split()[3]
        min_alpha = alpha.getextrema()[0]
        has_transparency = min_alpha < 250
    except Exception:
        return logo_url

    if has_transparency:
        print(f"  [logo] Already has transparency — using as-is: {os.path.basename(abs_path)}")
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
        else:
            print(f"  [logo] Background removal failed, using original. stderr: {result.stderr[:200]}")
            return logo_url
    except Exception as exc:
        print(f"  [logo] Could not run remove_bg.py: {exc}. Using original.")
        return logo_url



def _build_style_css(style: dict, selector_prefix: str = "") -> str:
    """
    Generate scoped CSS from a CardStyle JSON object.
    selector_prefix: e.g. '.style-card[data-style="glass_teal"]' for gallery
                     or  '.style-row.s-glass_teal'              for matrix
    """
    sid = style["id"]
    bg = style.get("card_bg", "#111")
    border = style.get("card_border", "1px solid rgba(255,255,255,0.1)")
    shadow = style.get("card_shadow", "none")
    radius = "0px"  # Force sharp rectangular corners for print-ready cards
    accent_line = style.get("accent_line", "")
    glow_before = style.get("glow_before", "")
    glow_after = style.get("glow_after", "")
    text_primary = style.get("text_primary", "#fff")
    text_secondary = style.get("text_secondary", "#aaa")
    text_accent = style.get("text_accent", "#00d2ff")
    text_label = style.get("text_label", "rgba(255,255,255,0.35)")
    divider_color = style.get("divider_color", "rgba(255,255,255,0.1)")
    logo_blend = style.get("logo_blend", "normal")
    logo_radius = style.get("logo_radius", "8px")
    font_headers = style.get("font_headers", "'Space Grotesk', sans-serif")
    font_body = style.get("font_body", "sans-serif")

    p = selector_prefix

    css = f"""
/* ── Style: {style.get('name', sid)} ── */
{p} .biz-card {{
  background: {bg};
  border: {border};
  box-shadow: {shadow};
  border-radius: {radius};
}}"""

    if accent_line:
        css += f"""
{p} .biz-card::before {{
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 100%; height: 10px;
  background: {accent_line};
  z-index: 2;
}}"""
    elif glow_before:
        css += f"""
{p} .biz-card::before {{
  content: '';
  position: absolute;
  width: 500px; height: 500px;
  background: {glow_before};
  top: -160px; left: -160px;
  pointer-events: none;
}}"""

    if glow_after:
        css += f"""
{p} .biz-card::after {{
  content: '';
  position: absolute;
  width: 400px; height: 400px;
  background: {glow_after};
  bottom: -140px; right: -140px;
  pointer-events: none;
}}"""

    css += f"""
{p} .card-company,
{p} .back-name {{
  color: {text_primary};
  font-family: {font_headers};
}}
{p} .card-tagline,
{p} .back-info-val {{
  color: {text_secondary};
  font-family: {font_body};
}}
{p} .back-role {{
  color: {text_accent};
  font-family: {font_body};
}}
{p} .back-info-label {{
  color: {text_label};
  font-family: {font_body};
}}
{p} .back-right {{
  border-left-color: {divider_color};
}}
{p} .card-logo img {{
  mix-blend-mode: {logo_blend};
  border-radius: {logo_radius};
  background: transparent;
}}

/* ── Layout Rules for {sid} ── */
{p} .card-front.layout-asymmetric {{
  flex-direction: row;
  justify-content: space-between;
  align-items: flex-end;
  padding: 60px;
  width: 100%; height: 100%;
}}
{p} .card-front.layout-asymmetric .card-logo {{
  position: absolute;
  top: 60px; left: 60px;
}}
{p} .card-front.layout-asymmetric .front-text-block {{
  text-align: right;
  margin-left: auto;
}}
{p} .card-back.layout-asymmetric {{
  flex-direction: row-reverse;
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: space-between;
  padding: 60px; gap: 40px;
}}
{p} .card-back.layout-asymmetric .back-right {{
  align-items: flex-start;
  padding-left: 0;
  padding-right: 40px;
  border-left: none;
  border-right: 1px solid {divider_color};
}}
{p} .card-back.layout-asymmetric .back-left {{
  align-items: flex-end;
}}
{p} .card-back.layout-asymmetric .back-info-row {{
  align-items: flex-end;
}}

{p} .card-front.layout-vertical {{
  flex-direction: row;
  padding: 0;
  align-items: stretch;
  width: 100%; height: 100%;
}}
{p} .card-front.layout-vertical .front-sidebar {{
  width: 200px;
  background: {text_accent};
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
  writing-mode: vertical-rl;
  text-transform: uppercase;
  letter-spacing: 2px;
  font-family: {font_headers};
  font-size: 2.2rem;
  font-weight: 700;
  color: {bg};
}}
{p} .card-front.layout-vertical .front-main {{
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 60px;
  gap: 20px;
}}

{p} .card-front.layout-minimal-line {{
  gap: 10px;
  width: 100%; height: 100%;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}}
{p} .card-front.layout-minimal-line .card-divider {{
  width: 140px;
  height: 2px;
  background: {text_accent};
  margin: 10px 0;
}}
{p} .card-back.layout-minimal-line {{
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: space-between;
  padding: 60px; gap: 40px;
}}
{p} .card-back.layout-minimal-line .back-left {{
  border-right: 1px solid {divider_color};
  padding-right: 40px;
}}
{p} .card-back.layout-minimal-line .back-right {{
  border-left: none;
  padding-left: 0;
}}

{p} .card-front.layout-split-color {{
  flex-direction: row;
  padding: 0;
  align-items: stretch;
  width: 100%; height: 100%;
}}
{p} .card-front.layout-split-color .split-left {{
  width: 40%;
  background: {text_accent};
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
}}
{p} .card-front.layout-split-color .split-right {{
  width: 60%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  padding: 60px;
  text-align: left;
}}
{p} .card-front.layout-split-color .split-right .card-company {{
  text-align: left;
}}
{p} .card-back.layout-split-color {{
  width: 100%; height: 100%;
  display: flex; align-items: center; justify-content: space-between;
  padding: 60px; gap: 40px;
}}
{p} .card-back.layout-split-color .split-left {{
  border-right: 1px solid {divider_color};
  padding-right: 40px;
}}
{p} .card-back.layout-split-color .split-right {{
  border-left: none;
  padding-left: 0;
}}
"""
    if style and "custom_css" in style:
        css += f"\n/* ── Custom CSS for {sid} ── */\n"
        css += style["custom_css"].replace("{{P}}", selector_prefix)

    return css


def _build_card_front_html(member: dict, company: str, logo_url: str, tagline: str, uid: str, style: dict = None) -> str:
    """Build the card-front inner HTML, using style templates if available."""
    logo_fallback_id = f"logo-fb-{uid}"
    tagline_html = f"<div class='card-tagline'>{tagline}</div>" if tagline else ""
    layout = style.get("layout", "classic") if style else "classic"

    # If the style has a custom HTML template, evaluate it
    if style and "front_html" in style:
        html = style["front_html"]
        html = html.replace("{{LOGO_URL}}", logo_url)
        html = html.replace("{{COMPANY}}", company)
        html = html.replace("{{TAGLINE}}", tagline_html)
        html = html.replace("{{LOGO_FALLBACK_ID}}", logo_fallback_id)
        html = html.replace("{{UID}}", uid)
        return html

    if layout == "asymmetric":
        return f"""
        <div class="card-front layout-asymmetric">
            <div class="card-logo">
                <img src="{logo_url}" alt="{company} logo"
                     onerror="this.style.display='none';document.getElementById('{logo_fallback_id}').style.display='block';">
                <div class="card-company" id="{logo_fallback_id}" style="display:none;">{company}</div>
            </div>
            <div class="front-text-block">
                <div class="card-company">{company}</div>
                {tagline_html}
            </div>
        </div>"""
    elif layout == "vertical":
        return f"""
        <div class="card-front layout-vertical">
            <div class="front-sidebar">
                <div class="sidebar-rotated-text">{company}</div>
            </div>
            <div class="front-main">
                <div class="card-logo">
                    <img src="{logo_url}" alt="{company} logo"
                         onerror="this.style.display='none';document.getElementById('{logo_fallback_id}').style.display='block';">
                    <div class="card-company" id="{logo_fallback_id}" style="display:none;">{company}</div>
                </div>
                {tagline_html}
            </div>
        </div>"""
    elif layout == "minimal_line":
        return f"""
        <div class="card-front layout-minimal-line">
            <div class="card-logo">
                <img src="{logo_url}" alt="{company} logo"
                     onerror="this.style.display='none';document.getElementById('{logo_fallback_id}').style.display='block';">
                    <div class="card-company" id="{logo_fallback_id}" style="display:none;">{company}</div>
            </div>
            <div class="card-divider"></div>
            <div class="card-company">{company}</div>
            {tagline_html}
        </div>"""
    elif layout == "split_color":
        return f"""
        <div class="card-front layout-split-color">
            <div class="split-left">
                <div class="card-logo">
                    <img src="{logo_url}" alt="{company} logo"
                         onerror="this.style.display='none';document.getElementById('{logo_fallback_id}').style.display='block';">
                    <div class="card-company" id="{logo_fallback_id}" style="display:none;">{company}</div>
                </div>
            </div>
            <div class="split-right">
                <div class="card-company">{company}</div>
                {tagline_html}
            </div>
        </div>"""
    else: # classic
        return f"""
        <div class="card-front layout-classic">
            <div class="card-logo">
                <img src="{logo_url}" alt="{company} logo"
                     onerror="this.style.display='none';document.getElementById('{logo_fallback_id}').style.display='block';">
                <div class="card-company" id="{logo_fallback_id}" style="display:none;">{company}</div>
            </div>
            <div class="card-company">{company}</div>
            {tagline_html}
        </div>"""


def _build_card_back_html(member: dict, company: str, contact: dict, style: dict = None) -> str:
    """Build the card-back inner HTML with flexible custom fields."""
    phone = member.get("phone") or contact.get("phone", "")
    email = member.get("email") or contact.get("email", "")
    website = member.get("website") or contact.get("website", "")
    custom_fields = member.get("custom_fields", {})
    layout = style.get("layout", "classic") if style else "classic"

    info_rows = ""
    if email:
        info_rows += f"""<div class="back-info-row">
            <span class="back-info-label">Email</span>
            <span class="back-info-val">{email}</span>
        </div>"""
    if phone:
        info_rows += f"""<div class="back-info-row">
            <span class="back-info-label">Phone</span>
            <span class="back-info-val">{phone}</span>
        </div>"""
    if website:
        info_rows += f"""<div class="back-info-row">
            <span class="back-info-label">Website</span>
            <span class="back-info-val">{website}</span>
        </div>"""
    for label, val in custom_fields.items():
        info_rows += f"""<div class="back-info-row">
            <span class="back-info-label">{label}</span>
            <span class="back-info-val">{val}</span>
        </div>"""

    # If the style has a custom HTML template, evaluate it
    if style and "back_html" in style:
        html = style["back_html"]
        html = html.replace("{{NAME}}", member['name'])
        html = html.replace("{{ROLE}}", member['role'])
        html = html.replace("{{COMPANY}}", company)
        html = html.replace("{{INFO_ROWS}}", info_rows)
        return html

    if layout == "asymmetric":
        return f"""
        <div class="card-back layout-asymmetric">
            <div class="back-left">{info_rows}</div>
            <div class="back-right">
                <div class="back-name">{member['name']}</div>
                <div class="back-role">{member['role']}</div>
                <div class="back-company-tag">{company}</div>
            </div>
        </div>"""
    elif layout == "vertical" or layout == "minimal_line" or layout == "split_color":
        return f"""
        <div class="card-back layout-{layout}">
            <div class="back-left">
                <div class="back-name">{member['name']}</div>
                <div class="back-role">{member['role']}</div>
                <div class="back-company-tag">{company}</div>
            </div>
            <div class="back-right">{info_rows}</div>
        </div>"""
    else: # classic
        return f"""
        <div class="card-back layout-classic">
            <div class="back-left">
                <div class="back-name">{member['name']}</div>
                <div class="back-role">{member['role']}</div>
                <div class="back-company-tag">{company}</div>
            </div>
            <div class="back-right">{info_rows}</div>
        </div>"""


# ─────────────────────────────────────────────────────────────────
#  GALLERY GENERATOR
# ─────────────────────────────────────────────────────────────────

def generate_gallery(profile_name: str):
    """Render the style gallery HTML."""
    state = load_state(profile_name)
    company = state.get("company", profile_name.upper())
    logo_url = state.get("logo_url", "")
    force_remove = state.get("remove_logo_background", False)
    logo_url = ensure_logo_no_bg(profile_name, logo_url, force_remove=force_remove)  # strip only if requested
    html_logo_url = f"../{logo_url}" if logo_url and not logo_url.startswith("http") else logo_url

    tagline = state.get("tagline", "")
    contact = state.get("contact", {})
    round_num = state.get("round", 1)
    team = state.get("team", [])
    sample_member = team[0] if team else {
        "name": "Your Name", "role": "Your Role",
        "email": contact.get("email", ""), "phone": contact.get("phone", ""),
        "website": contact.get("website", ""), "custom_fields": {}
    }

    # Use AI-generated styles if present, else fall back to defaults
    card_styles = state.get("card_styles") or DEFAULT_CARD_STYLES

    # Generate per-style scoped CSS
    all_style_css = ""
    seen_imports = set()
    for style in card_styles:
        fimport = style.get("font_import", "")
        if fimport and fimport not in seen_imports:
            all_style_css += fimport + "\n"
            seen_imports.add(fimport)

    for style in card_styles:
        sid = style["id"]
        prefix = f'.style-card[data-style="{sid}"] .card-preview-row'
        all_style_css += _build_style_css(style, prefix)

    # Build style card HTML blocks
    styles_html = ""
    liked = set(state.get("liked_card_styles", []))
    for style in card_styles:
        sid = style["id"]
        layout = style.get("layout", "classic")
        is_liked = sid in liked
        front_uid = f"gal-{sid}-front"
        back_uid = f"gal-{sid}-back"
        front_inner = _build_card_front_html(sample_member, company, html_logo_url, tagline, front_uid, style=style)
        back_inner = _build_card_back_html(sample_member, company, contact, style=style)
        selected_class = "selected" if is_liked else ""
        btn_class = "active" if is_liked else ""
        btn_label = "<span>❤️</span> Selected" if is_liked else "<span>🤍</span> Select Style"
        styles_html += f"""
    <div class="style-card {selected_class}" id="style-card-{sid}" data-style="{sid}">
        <div class="style-card-header">
            <span class="style-name">{style['name']} (Layout: {layout.upper()})</span>
            <span class="style-round">Round {round_num}</span>
        </div>
        <div class="card-preview-row">
            <div class="card-preview-wrap">
                <span class="preview-label">Front</span>
                <div class="biz-card l-{layout}">{front_inner}</div>
            </div>
            <div class="card-preview-wrap">
                <span class="preview-label">Back</span>
                <div class="biz-card l-{layout}">{back_inner}</div>
            </div>
        </div>
        <div class="style-card-footer">
            <button id="select-btn-{sid}" class="select-btn {btn_class}" onclick="toggleStyle('{sid}')">
                {btn_label}
            </button>
        </div>
    </div>"""

    with open(os.path.join(TEMPLATES_DIR, "style_gallery.html"), "r", encoding="utf-8") as f:
        template = f.read()

    rendered = template
    rendered = rendered.replace("{{COMPANY}}", company)
    rendered = rendered.replace("{{ROUND}}", str(round_num))
    rendered = rendered.replace("{{STYLES_HTML}}", styles_html)
    rendered = rendered.replace("{{SAMPLE_MEMBER_JSON}}", json.dumps(sample_member))
    rendered = rendered.replace("{{DYNAMIC_STYLE_CSS}}", all_style_css)

    out_dir = os.path.join(WORKSPACE_DIR, "grillbiz-profiles", profile_name, "cards")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{profile_name}_style_gallery.html")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Success: Generated style gallery at {out_path}")


# ─────────────────────────────────────────────────────────────────
#  CARD MATRIX GENERATOR
# ─────────────────────────────────────────────────────────────────

def generate_cards(profile_name: str):
    """Render the final team × styles card matrix HTML."""
    state = load_state(profile_name)
    company = state.get("company", profile_name.upper())
    logo_url = state.get("logo_url", "")
    force_remove = state.get("remove_logo_background", False)
    logo_url = ensure_logo_no_bg(profile_name, logo_url, force_remove=force_remove)  # strip only if requested

    html_logo_url = f"../{logo_url}" if logo_url and not logo_url.startswith("http") else logo_url
    tagline = state.get("tagline", "")
    contact = state.get("contact", {})
    team = state.get("team", [])
    liked_style_ids = state.get("liked_card_styles", [])
    all_card_styles = state.get("card_styles") or DEFAULT_CARD_STYLES

    if not liked_style_ids:
        liked_styles = all_card_styles
    else:
        style_map = {s["id"]: s for s in all_card_styles}
        liked_styles = [style_map[sid] for sid in liked_style_ids if sid in style_map]

    if not team:
        print("Error: No team members in state.json. Add team data first.")
        sys.exit(1)

    # Generate scoped CSS for all liked styles (scoped by .style-row.s-{id})
    all_style_css = ""
    seen_imports = set()
    for style in liked_styles:
        fimport = style.get("font_import", "")
        if fimport and fimport not in seen_imports:
            all_style_css += fimport + "\n"
            seen_imports.add(fimport)

    for style in liked_styles:
        prefix = f'.style-row.s-{style["id"]}'
        all_style_css += _build_style_css(style, prefix)

    # Build cards_data JSON for JS (used by downloadAll)
    cards_data = []
    for member in team:
        mid = member["name"].lower().replace(" ", "_").replace(".", "")
        cards_data.append({
            "id": mid,
            "name": member["name"],
            "role": member["role"],
            "styles": [{"id": s["id"], "name": s["name"]} for s in liked_styles]
        })

    # Build member tabs HTML
    tabs_html = ""
    for member, cd in zip(team, cards_data):
        tabs_html += f'<li data-member="{cd["id"]}"><a href="#member-{cd["id"]}" aria-current="false">{member["name"]}</a></li>\n'

    # Build member sections HTML
    members_html = ""
    for member, cd in zip(team, cards_data):
        mid = cd["id"]
        style_rows_html = ""
        for style in liked_styles:
            layout = style.get("layout", "classic")
            front_uid = f"{mid}-{style['id']}-front"
            back_uid = f"{mid}-{style['id']}-back"
            fn_front = f"{mid}_{style['id']}_front"
            fn_back = f"{mid}_{style['id']}_back"
            front_inner = _build_card_front_html(member, company, html_logo_url, tagline, front_uid, style=style)
            back_inner = _build_card_back_html(member, company, contact, style=style)
            style_rows_html += f"""
            <div class="style-row s-{style['id']}">
                <div class="style-row-header">
                    <span class="style-tag">{style['name']} (Layout: {layout.upper()})</span>
                    <div class="style-download-pair">
                        <button class="save-btn" onclick="saveCard('card-{front_uid}','{fn_front}')">
                            <span>📥</span> Front PNG
                        </button>
                        <button class="save-btn" onclick="saveCard('card-{back_uid}','{fn_back}')">
                            <span>📥</span> Back PNG
                        </button>
                    </div>
                </div>
                <div class="card-pair">
                    <div class="card-wrap">
                        <span class="card-side-label">Front</span>
                        <div class="biz-card l-{layout}" id="card-{front_uid}">{front_inner}</div>
                    </div>
                    <div class="card-wrap">
                        <span class="card-side-label">Back</span>
                        <div class="biz-card l-{layout}" id="card-{back_uid}">{back_inner}</div>
                    </div>
                </div>
            </div>"""

        members_html += f"""
        <section class="member-section" id="member-{mid}" data-member-id="{mid}" aria-label="{member['name']}">
            <div class="member-heading">
                <h2 class="member-name-heading">{member['name']}</h2>
                <span class="member-role-heading">{member['role']}</span>
            </div>
            <div class="style-rows">{style_rows_html}</div>
        </section>"""

    with open(os.path.join(TEMPLATES_DIR, "card_template.html"), "r", encoding="utf-8") as f:
        template = f.read()

    rendered = template
    rendered = rendered.replace("{{COMPANY}}", company)
    rendered = rendered.replace("{{MEMBER_TABS_HTML}}", tabs_html)
    rendered = rendered.replace("{{MEMBERS_HTML}}", members_html)
    rendered = rendered.replace("{{CARDS_DATA_JSON}}", json.dumps(cards_data))
    rendered = rendered.replace("{{DYNAMIC_STYLE_CSS}}", all_style_css)

    out_dir = os.path.join(WORKSPACE_DIR, "grillbiz-profiles", profile_name, "cards")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{profile_name}_cards.html")

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"Success: Generated card matrix at {out_path}")


# ─────────────────────────────────────────────────────────────────
#  ENTRYPOINT
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import shutil
    if not shutil.which("uipro"):
        print("=" * 60)
        print("ERROR: Dependency 'ui-ux-pro-max-cli' is not installed or not in PATH!")
        print("To install it, please run:")
        print("  npm install -g ui-ux-pro-max-cli")
        print("=" * 60)
        sys.exit(1)

    if len(sys.argv) < 3:
        print("Usage: python3 grill-card/card_parser.py <profile_name> gallery|cards")
        sys.exit(1)

    profile_name = sys.argv[1]
    mode = sys.argv[2].lower()

    if mode == "gallery":
        generate_gallery(profile_name)
    elif mode == "cards":
        generate_cards(profile_name)
    else:
        print(f"Error: Unknown mode '{mode}'. Use 'gallery' or 'cards'.")
        sys.exit(1)
