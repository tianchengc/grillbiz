#!/bin/bash

# Cloudflare Pages deployment helper script for GrillBiz
# Usage: ./deploy.sh <directory_to_deploy> <project_name>

DEPLOY_DIR="$1"
PROJECT_NAME="$2"

if [ -z "$DEPLOY_DIR" ] || [ -z "$PROJECT_NAME" ]; then
    echo "Usage: ./deploy.sh <directory_to_deploy> <project_name>"
    exit 1
fi

# Load root .env if it exists
if [ -f "../../.env" ]; then
    source "../../.env"
elif [ -f ".env" ]; then
    source ".env"
fi

# Check for Wrangler installation
if ! npx wrangler --version &>/dev/null; then
    echo "Wrangler is not installed. Installing and running wrangler..."
fi

# Determine deployment method
if [ -n "$CLOUDFLARE_API_TOKEN" ] && [ -n "$CLOUDFLARE_ACCOUNT_ID" ]; then
    echo "Found Cloudflare credentials in .env. Deploying automatically..."
    export CLOUDFLARE_API_TOKEN="$CLOUDFLARE_API_TOKEN"
    export CLOUDFLARE_ACCOUNT_ID="$CLOUDFLARE_ACCOUNT_ID"
    npx wrangler pages deploy "$DEPLOY_DIR" --project-name="$PROJECT_NAME"
else
    echo "Cloudflare credentials not found in .env."
    echo "Running Wrangler interactive deployment (this will prompt you to log into Cloudflare via your browser)..."
    npx wrangler pages deploy "$DEPLOY_DIR" --project-name="$PROJECT_NAME"
fi
