# 🗺️ GrillBiz — AI-Powered Startup Bootstrapper & Asset Generator

[![GitHub stars](https://img.shields.io/github/stars/tianchengc/grillbiz.svg?style=flat-round&color=orange)](https://github.com/tianchengc/grillbiz/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![MCP Server](https://img.shields.io/badge/MCP-Server-blue)](https://modelcontextprotocol.io)

**GrillBiz** is a premium bundle of open-source business helper skills and a **Model Context Protocol (MCP)** server designed to help solo developers, indie hackers, and founders bootstrap and manage their businesses directly from their AI assistant. 

With GrillBiz, you can subject every business idea to a thorough vetting "**grill**" and generate custom, stunning visual assets (brand names, logos, business cards, bio landing pages, and social media posts) without rigid templates.

---

## 🚀 The Core Philosophy: AI-Driven Design + Clean Layout Wrappers

Unlike traditional builders that force you into restrictive templates, GrillBiz uses a hybrid architecture:
1. **Dynamic AI-Driven Creation (No Limits):** Brand naming, logo prompts, and business card HTML/CSS layouts are crafted dynamically by your AI agent from scratch, allowing for fully customized brand expressions.
2. **Polished Display Templates:** Standardized visual showcase pages (the Lean Canvas grid, logo catalog, card gallery, and team matrix) provide interactive preview containers complete with dark/light mode toggles, local downloads, and pre-formatted feedback loops.

---

## ⚡ Quick Start & Installation

GrillBiz integrates seamlessly as an MCP server with **Claude Desktop**, **Cursor**, **Windsurf**, or other compatible AI assistants.

### Prerequisites
* **Python 3.10 or higher** (Required for the Model Context Protocol SDK).

### One-Command Installer (macOS & Linux)
To clone the repository and run the automated installer, copy and paste this command into your terminal:
```bash
git clone https://github.com/tianchengc/grillbiz.git && cd grillbiz && ./install.sh
```

This installer script will:
1. Verify Python version requirements.
2. Install Python dependencies (`mcp`, `playwright`, `pillow`).
3. Set up the headless browser Chromium for Playwright PNG exports.
4. Auto-register the GrillBiz MCP server inside your local **Claude Desktop** config file.

---

## 🔌 Manual MCP Integration

### Cursor
Add a new MCP server in Cursor settings:
* **Name:** `grillbiz`
* **Type:** `command`
* **Command:** `python3 -m mcp_server.py` (pointing to the absolute path of `mcp_server.py` in your clone).

### Claude Desktop
If the installer didn't run or you want to verify your config, add this block to your Claude Desktop config JSON (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):
```json
{
  "mcpServers": {
    "grillbiz": {
      "command": "python3",
      "args": ["/absolute/path/to/grillbiz/mcp_server.py"]
    }
  }
}
```

---

## 🧰 Skills Included

### 1. 📊 Strategic Business Analysis: `grill-biz` (Prompt: `grill_biz_workflow`)
* **Features:** A guided 9-block Lean Canvas self-interview. The agent reviews and critiques your answers (e.g., rejecting vague value propositions or overly broad target segments). Parses the markdown and outputs a stunning, interactive visual canvas HTML grid with a dark/light mode toggle.
* **Outputs:** 
  * Profile Markdown: `grillbiz-profiles/{profile_name}.md`
  * Active Canvas: `LEAN_CANVAS.md` (copied to root)
  * Visual Grid Page: `grillbiz-profiles/web/{profile_name}.html`

### 2. 🏷️ Taste-Trained Brand Naming: `grill-name` (Prompt: `grill_name_workflow`)
* **Features:** Guided naming profiling with a **5-round taste training phase** (picking preferred styles) to build your custom brand persona. Generates 20 custom candidates, performs WHOIS queries via raw TCP sockets, runs DNS resolution checks, scans trademark risks, and provides registrar routing.
* **Check Tool:** `check_domain`

### 3. 🎨 Brand Logo design: `grill-logo` (Prompt: `grill_logo_workflow`)
* **Features:** Generates 3 parallel visual concepts using image generation tools based on your brand core. Compiles them into a catalog. Includes a **Copy Feedback Prompt** button to easily refine and generate further rounds.
* **Outputs:**
  * Logo images: `grillbiz-profiles/{profile_name}/logos/logo_{round}_{idx}.png`
  * Visual Catalog Page: `grillbiz-profiles/{profile_name}/{profile_name}_logos.html`
* **Compile Tool:** `compile_logo_catalog`

### 4. 📇 Hero-Section Business Cards: `grill-card` (Prompt: `grill_card_workflow`)
* **Features:** Custom-crafted business cards styled like ecommerce landing page hero sections (full-bleed backgrounds, glassmorphism, or bold editorial type). Includes **automatic logo background detection and white-to-alpha removal**. Renders the front/back card layouts into a 10-style gallery and a multi-member team cards matrix.
* **Playwright Export:** Run the Playwright background script to crop and batch-export cards into high-resolution print-ready PNGs.
* **Outputs:**
  * Style Gallery Page: `grillbiz-profiles/{profile_name}/cards/{profile_name}_style_gallery.html`
  * Team Cards Matrix Page: `grillbiz-profiles/{profile_name}/cards/{profile_name}_cards.html`
* **Compile & Render Tools:** `compile_card_gallery`, `compile_card_matrix`, `render_business_cards`

### 🌳 5. Dynamic Next.js Bio Landing Website: `grill-bio` (Prompt: `grill_bio_workflow`)
* **Features:** Dynamic Next.js & Tailwind CSS v4 bio landing page (similar to Linktree but highly stylized). The AI agent writes the page React code from scratch under `grill-bio/boilerplate/` to match your brand colors and layout sections (socials, featured CTAs, products grid, lead capture form).
* **Deployment:** Contains an automated `deploy.sh` script to build and deploy to **Cloudflare Pages** instantly.

### 📸 6. Geo-Optimized Instagram Planner: `grill-post` (Prompt: `grill_post_workflow`)
* **Features:** Captures your active `LEAN_CANVAS.md` context to generate high-converting social media captions (hooks, local SEO, call-to-actions). Searches the Facebook Pages Places API to inject real location IDs and schedules posts directly via the API.

---

## 🛠️ Typical Bootstrapping Workflow

Once registered in your AI assistant, you can run through a complete startup bootstrapping flow in a single chat:

1. **Vet your business idea:**
   Ask your AI: `"Let's run through /grill-biz for a new organic tea shop called Chahaven"`
2. **Find available brand names:**
   Ask your AI: `"Let's run /grill-name to verify naming candidates and check available domains"`
3. **Design a visual logo:**
   Ask your AI: `"Let's run /grill-logo to generate brand logo ideas"`
4. **Create team business cards:**
   Ask your AI: `"Let's run /grill-card to design business cards for our team"`
5. **Generate and deploy a link website:**
   Ask your AI: `"Let's run /grill-bio to generate a modern bio landing page and deploy it to Cloudflare Pages"`

---

## 📝 License

GrillBiz is open-source software licensed under the [MIT License](LICENSE).
