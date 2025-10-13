#!/bin/bash

# RunPod Connection Script
# Connects to your RunPod instance via SSH

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/runpod_config.json"

# Check if jq is installed (for JSON parsing)
if ! command -v jq &> /dev/null; then
    echo "Installing jq for JSON parsing..."
    brew install jq
fi

# Read connection details from config
SSH_HOST=$(jq -r '.pod.ssh_host' "$CONFIG_FILE")
SSH_PORT=$(jq -r '.pod.ssh_port' "$CONFIG_FILE")
SSH_USER=$(jq -r '.pod.ssh_user' "$CONFIG_FILE")
SSH_KEY=$(jq -r '.pod.ssh_key_path' "$CONFIG_FILE" | sed "s|~|$HOME|")

POD_NAME=$(jq -r '.pod.name' "$CONFIG_FILE")
POD_ID=$(jq -r '.pod.id' "$CONFIG_FILE")

echo "======================================"
echo "Connecting to RunPod"
echo "======================================"
echo "Pod: $POD_NAME ($POD_ID)"
echo "Host: $SSH_HOST:$SSH_PORT"
echo "User: $SSH_USER"
echo "======================================"
echo ""

# Connect via SSH
ssh -i "$SSH_KEY" \
    -p "$SSH_PORT" \
    -o "StrictHostKeyChecking=no" \
    -o "UserKnownHostsFile=/dev/null" \
    "$SSH_USER@$SSH_HOST"
