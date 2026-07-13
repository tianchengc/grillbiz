#!/usr/bin/env python3
import os
import sys
import json
import shutil

WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROFILES_DIR = os.path.join(WORKSPACE_DIR, "grillbiz-profiles")

def migrate_old_profile(profile_name: str):
    """
    Migrates old split layout folders into the new unified layout:
    grillbiz-profiles/logos/{profile_name} -> grillbiz-profiles/{profile_name}/logos
    grillbiz-profiles/cards/{profile_name} -> grillbiz-profiles/{profile_name}/cards
    Merges their state.json files into grillbiz-profiles/{profile_name}/state.json.
    """
    profile_name = profile_name.strip().lower()
    unified_dir = os.path.join(PROFILES_DIR, profile_name)
    unified_state_file = os.path.join(unified_dir, "state.json")
    
    # Old directories
    old_logos_dir = os.path.join(PROFILES_DIR, "logos", profile_name)
    old_cards_dir = os.path.join(PROFILES_DIR, "cards", profile_name)
    
    # 1. Create unified directories
    unified_logos_dir = os.path.join(unified_dir, "logos")
    unified_cards_dir = os.path.join(unified_dir, "cards")
    
    # Check if we need to migrate
    if not os.path.exists(old_logos_dir) and not os.path.exists(old_cards_dir):
        return  # Nothing to migrate
        
    os.makedirs(unified_logos_dir, exist_ok=True)
    os.makedirs(unified_cards_dir, exist_ok=True)
    
    print(f"📦 Migrating profile '{profile_name}' to unified layout...")
    
    logos_data = []
    cards_state = {}
    
    # 2. Copy logos files and read state
    if os.path.exists(old_logos_dir):
        old_logos_state = os.path.join(old_logos_dir, "state.json")
        if os.path.exists(old_logos_state):
            try:
                with open(old_logos_state, "r", encoding="utf-8") as f:
                    logos_data = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to read old logos state.json: {e}")
                
        # Copy all image files
        for fname in os.listdir(old_logos_dir):
            if fname != "state.json" and fname.endswith(".png"):
                src_path = os.path.join(old_logos_dir, fname)
                dest_path = os.path.join(unified_logos_dir, fname)
                shutil.copy2(src_path, dest_path)
                
    # 3. Copy cards files and read state
    if os.path.exists(old_cards_dir):
        old_cards_state = os.path.join(old_cards_dir, "state.json")
        if os.path.exists(old_cards_state):
            try:
                with open(old_cards_state, "r", encoding="utf-8") as f:
                    cards_state = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to read old cards state.json: {e}")
                
        # Copy HTML files etc
        for fname in os.listdir(old_cards_dir):
            if fname != "state.json" and not os.path.isdir(os.path.join(old_cards_dir, fname)):
                src_path = os.path.join(old_cards_dir, fname)
                dest_path = os.path.join(unified_cards_dir, fname)
                shutil.copy2(src_path, dest_path)

    # 4. Merge states if unified state doesn't exist yet
    if not os.path.exists(unified_state_file):
        merged_state = {
            "profile": profile_name,
            "company": cards_state.get("company", profile_name.upper()),
            "tagline": cards_state.get("tagline", ""),
            "contact": cards_state.get("contact", {"phone": "", "email": "", "website": ""}),
            "round": cards_state.get("round", 1),
            "liked_logo_ids": [l["id"] for l in logos_data if l.get("liked", False)],
            "liked_card_styles": cards_state.get("liked_styles", []),
            "liked_bio_styles": [],
            "logos": [],
            "card_styles": cards_state.get("card_styles", []),
            "bio_styles": [],
            "team": cards_state.get("team", []),
            "socials": [],
            "products": [],
            "blogs": []
        }
        
        # Rewrite logo paths in state
        for item in logos_data:
            # e.g., "logos/default/logo_1_1.png" -> "logos/logo_1_1.png"
            old_path = item["path"]
            filename = os.path.basename(old_path)
            item["path"] = f"logos/{filename}"
            merged_state["logos"].append(item)
            
        # Resolve logo_url relative to profile dir
        old_logo_url = cards_state.get("logo_url", "")
        if old_logo_url:
            filename = os.path.basename(old_logo_url)
            merged_state["logo_url"] = f"logos/{filename}"
        elif merged_state["liked_logo_ids"]:
            first_liked = merged_state["liked_logo_ids"][0]
            for l in merged_state["logos"]:
                if l["id"] == first_liked:
                    merged_state["logo_url"] = l["path"]
                    break
        else:
            merged_state["logo_url"] = ""
            
        with open(unified_state_file, "w", encoding="utf-8") as f:
            json.dump(merged_state, f, indent=2, ensure_ascii=False)
            
        print(f"✅ Created unified state.json at {unified_state_file}")
        
    # 5. Rename old directories to mark them as migrated
    try:
        if os.path.exists(old_logos_dir):
            os.rename(old_logos_dir, old_logos_dir + ".migrated")
        if os.path.exists(old_cards_dir):
            os.rename(old_cards_dir, old_cards_dir + ".migrated")
    except Exception as e:
        print(f"Warning: Could not rename old directories: {e}")

def load_profile_state(profile_name: str) -> dict:
    """Loads state.json for the specified profile (performing migration if necessary)."""
    profile_name = profile_name.strip().lower()
    migrate_old_profile(profile_name)
    
    state_file = os.path.join(PROFILES_DIR, profile_name, "state.json")
    if not os.path.exists(state_file):
        # Return default blank profile state
        return {
            "profile": profile_name,
            "company": profile_name.upper(),
            "tagline": "",
            "contact": {"phone": "", "email": "", "website": ""},
            "round": 1,
            "liked_logo_ids": [],
            "liked_card_styles": [],
            "liked_bio_styles": [],
            "logos": [],
            "card_styles": [],
            "bio_styles": [],
            "team": [],
            "socials": [],
            "products": [],
            "blogs": []
        }
        
    with open(state_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_profile_state(profile_name: str, state: dict):
    """Saves the state.json for the specified profile."""
    profile_name = profile_name.strip().lower()
    profile_dir = os.path.join(PROFILES_DIR, profile_name)
    os.makedirs(profile_dir, exist_ok=True)
    
    state_file = os.path.join(profile_dir, "state.json")
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

def list_profiles() -> list:
    """Lists all available business profiles."""
    if not os.path.exists(PROFILES_DIR):
        return []
    
    profiles = []
    ignored = {"logos", "cards", "bio", "homepage"}
    for name in os.listdir(PROFILES_DIR):
        full_path = os.path.join(PROFILES_DIR, name)
        if os.path.isdir(full_path) and name not in ignored and not name.endswith(".migrated"):
            # Ensure state.json exists or it's a valid directory
            if os.path.exists(os.path.join(full_path, "state.json")):
                profiles.append(name)
    return sorted(profiles)

def select_profile(profile_name: str = None) -> str:
    """
    Resolves the active profile name. If none is provided, it tries to auto-detect.
    If multiple exist, it returns None to signal the caller to prompt the user.
    """
    if profile_name:
        return profile_name.strip().lower()
        
    profiles = list_profiles()
    if len(profiles) == 1:
        return profiles[0]
    elif len(profiles) == 0:
        return "default"
    else:
        return None  # Signal ambiguity
