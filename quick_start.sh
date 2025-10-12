#!/bin/bash

# SDXL Image Generator - Quick Start Script
# This script provides easy examples for getting started

echo "=========================================="
echo "SDXL Image Generator - Quick Start"
echo "=========================================="
echo ""

# Activate virtual environment
source venv/bin/activate

echo "Virtual environment activated!"
echo ""
echo "Available commands:"
echo ""
echo "1. Basic generation (no LoRA):"
echo '   python generate.py --prompt "a beautiful landscape"'
echo ""
echo "2. With custom size and steps:"
echo '   python generate.py --prompt "portrait of a person" --width 768 --height 1024 --steps 40'
echo ""
echo "3. With LoRA:"
echo '   python generate.py --prompt "your prompt" --lora ./loras/your_lora.safetensors --lora-scale 0.8'
echo ""
echo "4. Using config file:"
echo '   python generate_with_config.py --prompt "your prompt" --preset quality'
echo ""
echo "5. Batch generation with seed:"
echo '   python generate.py --prompt "your prompt" --num-images 4 --seed 42'
echo ""
echo "=========================================="
echo ""

# Check if user wants to run a test
read -p "Do you want to run a test generation? (Note: First run will download ~7GB model) [y/N]: " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo ""
    echo "Running test generation..."
    echo "This will generate a 512x512 test image with minimal steps."
    echo ""

    python generate.py \
        --prompt "a cute cat sitting on a desk, professional photography" \
        --negative-prompt "blurry, low quality" \
        --width 512 \
        --height 512 \
        --steps 20 \
        --guidance-scale 7.0

    echo ""
    echo "Test complete! Check the outputs/ folder for your image."
else
    echo "Skipping test generation."
    echo "Run the commands above to generate images!"
fi

echo ""
echo "For more options, see README.md or run:"
echo "  python generate.py --help"
echo ""
