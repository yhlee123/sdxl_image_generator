#!/bin/bash

# Sync LoRA files to RunPod
# This script uploads your local LoRA files to the RunPod instance

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$SCRIPT_DIR/runpod_config.json"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo_info "Installing jq..."
    brew install jq
fi

# Read configuration
SSH_HOST=$(jq -r '.pod.ssh_host' "$CONFIG_FILE")
SSH_PORT=$(jq -r '.pod.ssh_port' "$CONFIG_FILE")
SSH_USER=$(jq -r '.pod.ssh_user' "$CONFIG_FILE")
SSH_KEY=$(jq -r '.pod.ssh_key_path' "$CONFIG_FILE" | sed "s|~|$HOME|")
REMOTE_DIR=$(jq -r '.deployment.remote_project_dir' "$CONFIG_FILE")
LORAS_DIR=$(jq -r '.deployment.loras_dir' "$CONFIG_FILE")

echo "======================================"
echo "Syncing LoRA Files to RunPod"
echo "======================================"
echo ""

# Check if local loras directory exists
if [ ! -d "$PROJECT_DIR/loras" ]; then
    echo_info "No local loras directory found. Creating it..."
    mkdir -p "$PROJECT_DIR/loras"
    echo "Please place your LoRA .safetensors files in: $PROJECT_DIR/loras/"
    exit 0
fi

# Count LoRA files
LORA_COUNT=$(find "$PROJECT_DIR/loras" -name "*.safetensors" | wc -l | tr -d ' ')

if [ "$LORA_COUNT" -eq 0 ]; then
    echo_info "No LoRA files found in $PROJECT_DIR/loras/"
    echo "Please add .safetensors files to sync."
    exit 0
fi

echo_info "Found $LORA_COUNT LoRA file(s) to sync"
echo ""

# Create remote loras directory
ssh -i "$SSH_KEY" -p "$SSH_PORT" -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null \
    "$SSH_USER@$SSH_HOST" "mkdir -p $LORAS_DIR"

# Sync LoRA files
echo_info "Uploading LoRA files..."
rsync -avz --progress \
    -e "ssh -i $SSH_KEY -p $SSH_PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
    --include="*.safetensors" \
    --exclude="*" \
    "$PROJECT_DIR/loras/" \
    "$SSH_USER@$SSH_HOST:$LORAS_DIR/"

echo ""
echo_info "LoRA sync complete! $LORA_COUNT file(s) uploaded."
echo ""
