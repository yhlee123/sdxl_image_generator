#!/bin/bash

# RunPod Deployment Script
# Deploys the SDXL image generator to your RunPod instance

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_FILE="$SCRIPT_DIR/runpod_config.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

echo_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

echo_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo_info "Installing jq for JSON parsing..."
    brew install jq
fi

# Read configuration
SSH_HOST=$(jq -r '.pod.ssh_host' "$CONFIG_FILE")
SSH_PORT=$(jq -r '.pod.ssh_port' "$CONFIG_FILE")
SSH_USER=$(jq -r '.pod.ssh_user' "$CONFIG_FILE")
SSH_KEY=$(jq -r '.pod.ssh_key_path' "$CONFIG_FILE" | sed "s|~|$HOME|")
REMOTE_DIR=$(jq -r '.deployment.remote_project_dir' "$CONFIG_FILE")
POD_NAME=$(jq -r '.pod.name' "$CONFIG_FILE")

SSH_CMD="ssh -i $SSH_KEY -p $SSH_PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null $SSH_USER@$SSH_HOST"
SCP_CMD="scp -i $SSH_KEY -P $SSH_PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null"

echo "======================================"
echo "Deploying to RunPod: $POD_NAME"
echo "======================================"
echo ""

# Step 1: Create remote directory
echo_info "Creating remote directory: $REMOTE_DIR"
$SSH_CMD "mkdir -p $REMOTE_DIR"

# Step 2: Sync project files (excluding venv, outputs, models, loras)
echo_info "Syncing project files to RunPod..."
rsync -avz --progress \
    -e "ssh -i $SSH_KEY -p $SSH_PORT -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null" \
    --exclude 'venv/' \
    --exclude 'outputs/' \
    --exclude 'models/' \
    --exclude 'loras/*.safetensors' \
    --exclude '__pycache__/' \
    --exclude '.git/' \
    --exclude '*.pyc' \
    "$PROJECT_DIR/" \
    "$SSH_USER@$SSH_HOST:$REMOTE_DIR/"

# Step 3: Setup Python environment on RunPod
echo_info "Setting up Python environment on RunPod..."
$SSH_CMD "cd $REMOTE_DIR && bash" << 'ENDSSH'
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        echo "Python3 not found! Please install Python3 on your RunPod instance."
        exit 1
    fi

    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi

    # Activate and install dependencies
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt

    # Install additional video generation dependencies
    echo "Installing video generation dependencies..."
    pip install opencv-python imageio imageio-ffmpeg

    echo "Setup complete!"
ENDSSH

# Step 4: Create necessary directories
echo_info "Creating required directories..."
$SSH_CMD "mkdir -p $REMOTE_DIR/{loras,models,outputs}"

echo ""
echo_info "Deployment complete!"
echo ""
echo "======================================"
echo "Next Steps:"
echo "======================================"
echo "1. Connect to RunPod: ./runpod/connect.sh"
echo "2. Upload your LoRA files to $REMOTE_DIR/loras/"
echo "3. Run generation: cd $REMOTE_DIR && source venv/bin/activate && python generate.py --prompt 'your prompt'"
echo ""
