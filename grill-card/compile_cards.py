#!/usr/bin/env python3
"""
grill-card/compile_cards.py
===========================
General-purpose compile script for Grill-Card.

Usage:
    python3 grill-card/compile_cards.py <profile_name>

Reads card_styles and liked_card_styles from:
    grillbiz-profiles/{profile}/state.json

Writes:
    grillbiz-profiles/{profile}/cards/{profile}_style_gallery.html
    grillbiz-profiles/{profile}/cards/{profile}_cards.html

The gallery shows:
  - "Your Favourites" section (accumulated liked styles across all rounds)
  - "Round N — New Designs" section (current round's card_styles)

The cards matrix shows only the current round's styles (or liked only if --liked-only flag).
"""

import json
import os
import sys

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(WORKSPACE_DIR, "grill-card", "templates")


def load_state(profile_name: str) -> dict:
    path = os.path.join(WORKSPACE_DIR, "grillbiz-profiles", profile_name, "state.json")
    if not os.path.exists(path):
        print(f"❌ state.json not found at: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_state(profile_name: str, state: dict):
    path = os.path.join(WORKSPACE_DIR, "grillbiz-profiles", profile_name, "state.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)


# ─────────────────────────────────────────────────────────────────
# LOGO PATH RESOLVER
# ─────────────────────────────────────────────────────────────────

def resolve_logo_url(profile_name: str, logo_url: str) -> str:
    """Return a relative URL suitable for HTML <img src=> from the cards/ output dir."""
    if not logo_url:
        return ""
    if logo_url.startswith("http"):
        return logo_url
    # logo_url is relative to profile root, e.g. "logos/logo_1_3_clean.png"
    # Cards output dir is: grillbiz-profiles/{profile}/cards/
    # So relative from there: ../logos/logo_1_3_clean.png
    return f"../{logo_url}"


# ─────────────────────────────────────────────────────────────────
# CSS COMPILER
# ─────────────────────────────────────────────────────────────────

def compile_style_css(style: dict, is_gallery: bool = False) -> str:
    sid = style["id"]
    bg = style.get("card_bg", "#ffffff")
    border = style.get("card_border", "none")
    shadow = style.get("card_shadow", "none")
    scope = f".s-{sid}"

    if is_gallery:
        sizing = f"""
        .style-card{scope} .biz-card {{
            width: 1050px !important; height: 600px !important;
            transform: scale(0.333333) !important; transform-origin: top center !important;
            margin-bottom: -400px !important; border-radius: 0px !important;
        }}"""
    else:
        sizing = f"""
        .style-row{scope} .biz-card {{
            width: 1050px !important; height: 600px !important;
            transform: scale(0.5) !important; transform-origin: top left !important;
            margin-bottom: -300px !important; margin-right: -525px !important; border-radius: 0px !important;
        }}"""

    base = f"""
    {scope}.biz-card {{ background: {bg} !important; border: {border} !important; box-shadow: {shadow} !important; }}
    """
    custom = style.get("custom_css", "").replace("{{P}}", scope)
    return sizing + base + custom


# ─────────────────────────────────────────────────────────────────
# HTML BUILDERS
# ─────────────────────────────────────────────────────────────────

def build_front_html(member: dict, company: str, logo_url: str, tagline: str,
                     uid: str, style: dict) -> str:
    tagline_html = f"<div class='card-tagline'>{tagline}</div>" if tagline else ""
    html = style["front_html"]
    html = html.replace("{{LOGO_URL}}", logo_url)
    html = html.replace("{{COMPANY}}", company)
    html = html.replace("{{TAGLINE}}", tagline_html)
    html = html.replace("{{UID}}", uid)
    return html


def build_back_html(member: dict, company: str, contact: dict, style: dict) -> str:
    email = member.get("email") or contact.get("email", "")
    phone = member.get("phone") or contact.get("phone", "")
    website = member.get("website") or contact.get("website", "")
    custom_fields = member.get("custom_fields", {})

    info_rows = ""
    for label, val in [("Email", email), ("Phone", phone), ("Website", website)]:
        if val:
            info_rows += (
                f'<div class="back-info-row">'
                f'<span class="back-info-label">{label}</span>'
                f'<span class="back-info-val">{val}</span>'
                f'</div>'
            )
    for label, val in custom_fields.items():
        if val:
            info_rows += (
                f'<div class="back-info-row">'
                f'<span class="back-info-label">{label}</span>'
                f'<span class="back-info-val">{val}</span>'
                f'</div>'
            )

    html = style["back_html"]
    html = html.replace("{{NAME}}", member.get("name", ""))
    html = html.replace("{{ROLE}}", member.get("role", ""))
    html = html.replace("{{COMPANY}}", company)
    html = html.replace("{{INFO_ROWS}}", info_rows)
    return html


def build_style_card_html(style: dict, member: dict, company: str, logo_url: str,
                           tagline: str, contact: dict, index: int,
                           round_num: int, is_liked: bool = False) -> str:
    """Build a single .style-card block for the gallery."""
    sid = style["id"]
    prefix = "liked" if is_liked else "new"
    fuid = f"{prefix}f{index}"
    buid = f"{prefix}b{index}"
    badge = " ❤️" if is_liked else ""
    front = build_front_html(member, company, logo_url, tagline, fuid, style)
    back = build_back_html(member, company, contact, style)
    return f"""
    <div class="style-card s-{sid}" id="style-card-{sid}">
        <div class="style-card-header">
            <span class="style-name">{style['name']}{badge}</span>
            <span class="style-round">Round {style.get('round', round_num)}</span>
        </div>
        <div class="card-preview-row">
            <div class="card-preview-wrap">
                <span class="preview-label">Front</span>
                <div class="biz-card s-{sid}" id="card-{fuid}">{front}</div>
            </div>
            <div class="card-preview-wrap">
                <span class="preview-label">Back</span>
                <div class="biz-card s-{sid}" id="card-{buid}">{back}</div>
            </div>
        </div>
        <div class="style-card-footer">
            <button id="select-btn-{sid}" class="select-btn" onclick="toggleStyle('{sid}')">
                <span>🤍</span> Select Style
            </button>
        </div>
    </div>"""


# ─────────────────────────────────────────────────────────────────
# GALLERY COMPILER
# ─────────────────────────────────────────────────────────────────

def compile_gallery(profile_name: str, state: dict):
    company = state.get("company", profile_name.capitalize())
    logo_url = resolve_logo_url(profile_name, state.get("logo_url", ""))
    tagline = state.get("tagline", "")
    contact = state.get("contact", {})
    team = state.get("team", [])
    round_num = state.get("round", 1)

    # Use first team member as sample for gallery preview
    sample = team[0] if team else {
        "name": "Your Name", "role": "Your Role",
        "email": contact.get("email", ""), "phone": contact.get("phone", ""),
        "website": contact.get("website", ""), "custom_fields": {}
    }

    current_styles = state.get("card_styles", [])
    liked_ids = set(state.get("liked_card_styles", []))
    # Liked style objects: from liked_card_styles_data (accumulated) or fallback to card_styles
    liked_style_data = state.get("liked_card_styles_data", [])
    # Also include any current styles that are already liked
    liked_ids_in_current = {s["id"] for s in current_styles if s["id"] in liked_ids}

    # Collect CSS (fonts + per-style)
    all_css = ""
    seen_fonts = set()

    # Gather all styles: liked + current
    all_styles_for_css = liked_style_data + current_styles
    for s in all_styles_for_css:
        fi = s.get("font_import", "")
        if fi and fi not in seen_fonts:
            all_css += fi + "\n"
            seen_fonts.add(fi)
    for s in all_styles_for_css:
        all_css += compile_style_css(s, is_gallery=True) + "\n"

    # Build liked styles HTML
    liked_styles_html = ""
    for i, s in enumerate(liked_style_data):
        liked_styles_html += build_style_card_html(
            s, sample, company, logo_url, tagline, contact, i, round_num, is_liked=True
        )

    # Build new round styles HTML (exclude ones already in liked section)
    new_styles_html = ""
    for i, s in enumerate(current_styles):
        new_styles_html += build_style_card_html(
            s, sample, company, logo_url, tagline, contact, i, round_num, is_liked=False
        )

    liked_section_display = "block" if liked_style_data else "none"

    with open(os.path.join(TEMPLATES_DIR, "style_gallery.html"), "r", encoding="utf-8") as f:
        tpl = f.read()

    rendered = (
        tpl
        .replace("{{COMPANY}}", company)
        .replace("{{STYLES_HTML}}", new_styles_html)
        .replace("{{LIKED_STYLES_HTML}}", liked_styles_html)
        .replace("{{LIKED_SECTION_DISPLAY}}", liked_section_display)
        .replace("{{DYNAMIC_STYLE_CSS}}", all_css)
        .replace("{{ROUND}}", str(round_num))
    )

    out_dir = os.path.join(WORKSPACE_DIR, "grillbiz-profiles", profile_name, "cards")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{profile_name}_style_gallery.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"✅ Gallery → {out_path}")
    return out_path


# ─────────────────────────────────────────────────────────────────
# CARDS MATRIX COMPILER
# ─────────────────────────────────────────────────────────────────

def compile_cards(profile_name: str, state: dict, liked_only: bool = False):
    company = state.get("company", profile_name.capitalize())
    logo_url = resolve_logo_url(profile_name, state.get("logo_url", ""))
    tagline = state.get("tagline", "")
    contact = state.get("contact", {})
    team = state.get("team", [])

    current_styles = state.get("card_styles", [])
    liked_ids = set(state.get("liked_card_styles", []))
    liked_style_data = state.get("liked_card_styles_data", [])

    # Decide which styles to render in the matrix
    if liked_only and liked_style_data:
        styles_to_render = liked_style_data
        print(f"  Rendering {len(styles_to_render)} liked styles only.")
    else:
        styles_to_render = current_styles
        print(f"  Rendering {len(styles_to_render)} current round styles.")

    if not team:
        print("⚠️  No team members found in state.json. Skipping cards matrix.")
        return None

    # Build CSS
    all_css = ""
    seen_fonts = set()
    for s in styles_to_render:
        fi = s.get("font_import", "")
        if fi and fi not in seen_fonts:
            all_css += fi + "\n"
            seen_fonts.add(fi)
    for s in styles_to_render:
        all_css += compile_style_css(s, is_gallery=False) + "\n"

    # Build member tabs + sections
    tabs_html = ""
    members_html = ""
    cards_data = []

    for idx, member in enumerate(team):
        mid = f"m-{idx}"
        active_class = "active" if idx == 0 else ""
        tabs_html += (
            f'<li class="{active_class}" id="tab-li-{mid}">'
            f'<a onclick="showMember(\'{mid}\')">{member["name"]}</a></li>\n'
        )
        rows = ""
        for si, s in enumerate(styles_to_render):
            sid = s["id"]
            fuid = f"front-{idx}-{si}"
            buid = f"back-{idx}-{si}"
            cards_data.append({
                "name": member["name"],
                "frontId": f"card-{fuid}",
                "backId": f"card-{buid}"
            })
            front = build_front_html(member, company, logo_url, tagline, fuid, s)
            back = build_back_html(member, company, contact, s)
            rows += f"""
            <div class="style-row s-{sid}">
                <div class="style-row-header">
                    <span class="style-tag">{s['name']}</span>
                    <div class="style-download-pair">
                        <button class="save-btn" onclick="saveCard('card-{fuid}','{mid}_{sid}_front')"><span>📥</span> Front PNG</button>
                        <button class="save-btn" onclick="saveCard('card-{buid}','{mid}_{sid}_back')"><span>📥</span> Back PNG</button>
                    </div>
                </div>
                <div class="card-pair">
                    <div class="card-wrap"><span class="card-side-label">Front</span><div class="biz-card s-{sid}" id="card-{fuid}">{front}</div></div>
                    <div class="card-wrap"><span class="card-side-label">Back</span><div class="biz-card s-{sid}" id="card-{buid}">{back}</div></div>
                </div>
            </div>"""

        members_html += f"""
        <section class="member-section {active_class}" id="member-{mid}" data-member-id="{mid}" aria-label="{member['name']}">
            <div class="member-heading">
                <h2 class="member-name-heading">{member['name']}</h2>
                <span class="member-role-heading">{member['role']}</span>
            </div>
            <div class="style-rows">{rows}</div>
        </section>"""

    with open(os.path.join(TEMPLATES_DIR, "card_template.html"), "r", encoding="utf-8") as f:
        tpl = f.read()

    rendered = (
        tpl
        .replace("{{COMPANY}}", company)
        .replace("{{MEMBER_TABS_HTML}}", tabs_html)
        .replace("{{MEMBERS_HTML}}", members_html)
        .replace("{{CARDS_DATA_JSON}}", json.dumps(cards_data))
        .replace("{{DYNAMIC_STYLE_CSS}}", all_css)
    )

    out_dir = os.path.join(WORKSPACE_DIR, "grillbiz-profiles", profile_name, "cards")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{profile_name}_cards.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    print(f"✅ Cards matrix → {out_path}")
    return out_path


# ─────────────────────────────────────────────────────────────────
# FEEDBACK HANDLER
# Saves liked style IDs + full objects to state, increments round.
# Call this when the agent reads a [GRILL-CARD FEEDBACK] prompt.
# ─────────────────────────────────────────────────────────────────

def apply_feedback(profile_name: str, liked_ids: list):
    """
    Record liked style IDs from the current round into state.json.
    - Adds IDs to liked_card_styles (deduplicated)
    - Copies full style objects into liked_card_styles_data
    - Increments round counter
    """
    state = load_state(profile_name)
    current_styles = {s["id"]: s for s in state.get("card_styles", [])}

    existing_liked_ids = set(state.get("liked_card_styles", []))
    existing_liked_data = {s["id"]: s for s in state.get("liked_card_styles_data", [])}

    for lid in liked_ids:
        if lid in current_styles:
            existing_liked_ids.add(lid)
            style_obj = dict(current_styles[lid])
            style_obj["round"] = state.get("round", 1)
            existing_liked_data[lid] = style_obj
        else:
            print(f"⚠️  Style ID '{lid}' not found in current card_styles — skipping.")

    state["liked_card_styles"] = sorted(existing_liked_ids)
    state["liked_card_styles_data"] = list(existing_liked_data.values())
    state["round"] = state.get("round", 1) + 1

    save_state(profile_name, state)
    print(f"✅ Saved {len(liked_ids)} liked style(s). Now on Round {state['round']}.")
    return state


# ─────────────────────────────────────────────────────────────────
# PROCEED HANDLER
# Call this when the agent reads a [GRILL-CARD PROCEED] prompt.
# Compiles the final cards matrix with ONLY the selected styles.
# ─────────────────────────────────────────────────────────────────

def apply_proceed(profile_name: str, final_ids: list):
    """
    Save final selected style IDs and compile the final cards matrix
    using ONLY those styles (from liked_card_styles_data).
    """
    state = load_state(profile_name)

    # Merge final selections into liked data if not already there
    current_styles = {s["id"]: s for s in state.get("card_styles", [])}
    existing_liked_data = {s["id"]: s for s in state.get("liked_card_styles_data", [])}
    existing_liked_ids = set(state.get("liked_card_styles", []))

    for fid in final_ids:
        if fid in current_styles and fid not in existing_liked_data:
            existing_liked_data[fid] = current_styles[fid]
            existing_liked_ids.add(fid)

    state["liked_card_styles"] = sorted(existing_liked_ids)
    state["liked_card_styles_data"] = list(existing_liked_data.values())
    # Filter liked_card_styles_data to only the final selected ones for the matrix
    state["_final_card_styles"] = [s for s in state["liked_card_styles_data"] if s["id"] in set(final_ids)]

    save_state(profile_name, state)

    # Build a temporary state with only final styles for the cards matrix
    final_state = dict(state)
    final_state["card_styles"] = state["_final_card_styles"]

    path = compile_cards(profile_name, final_state, liked_only=False)
    print(f"✅ Final cards compiled with {len(final_ids)} selected style(s): {', '.join(final_ids)}")
    return path


# ─────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 grill-card/compile_cards.py <profile_name> [--liked-only]")
        print("")
        print("Examples:")
        print("  python3 grill-card/compile_cards.py chahaven")
        print("  python3 grill-card/compile_cards.py chahaven --liked-only")
        sys.exit(1)

    profile = sys.argv[1]
    liked_only = "--liked-only" in sys.argv

    state = load_state(profile)

    print(f"\n📦 Compiling cards for profile: {profile}")
    print(f"   Round: {state.get('round', 1)}")
    print(f"   Current styles: {len(state.get('card_styles', []))}")
    print(f"   Liked styles: {len(state.get('liked_card_styles', []))}")
    print()

    gallery_path = compile_gallery(profile, state)
    cards_path = compile_cards(profile, state, liked_only=liked_only)

    print()
    print("🎨 Open in your browser:")
    print(f"   Style Gallery : file://{gallery_path}")
    if cards_path:
        print(f"   Team Cards    : file://{cards_path}")
