#!/usr/bin/env python3
"""
SDXL Generator using configuration file
"""

import argparse
import json
from pathlib import Path
from generate import SDXLGenerator


def load_config(config_path: str) -> dict:
    """Load configuration from JSON file."""
    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using SDXL with a configuration file"
    )

    parser.add_argument(
        "--config",
        type=str,
        default="./configs/example_config.json",
        help="Path to configuration file"
    )
    parser.add_argument(
        "--preset",
        type=str,
        default=None,
        help="Use a preset from the config (quick, quality, portrait, landscape, etc.)"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Text prompt for image generation"
    )
    parser.add_argument(
        "--negative-prompt",
        type=str,
        default=None,
        help="Negative prompt (overrides config)"
    )
    parser.add_argument(
        "--enable-lora",
        type=str,
        action="append",
        default=[],
        help="Enable specific LoRA by name from config (can specify multiple)"
    )
    parser.add_argument(
        "--num-images",
        type=int,
        default=1,
        help="Number of images to generate"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./outputs",
        help="Directory to save generated images"
    )

    args = parser.parse_args()

    # Load configuration
    config = load_config(args.config)
    print(f"Loaded configuration from: {args.config}")

    # Get model settings
    model_config = config.get("model", {})

    # Get generation defaults
    gen_defaults = config.get("generation_defaults", {})

    # Apply preset if specified
    if args.preset:
        presets = config.get("presets", {})
        if args.preset in presets:
            print(f"Using preset: {args.preset}")
            gen_defaults.update(presets[args.preset])
        else:
            print(f"Warning: Preset '{args.preset}' not found in config")

    # Create generator
    generator = SDXLGenerator(
        model_id=model_config.get("model_id", "stabilityai/stable-diffusion-xl-base-1.0"),
        vae_model=model_config.get("vae_model"),
        device=model_config.get("device", "mps"),
        dtype=model_config.get("dtype", "float16"),
        output_dir=args.output_dir
    )

    # Load enabled LoRAs
    loras = config.get("loras", {})
    loras_to_load = []

    # If specific LoRAs are requested, load those
    if args.enable_lora:
        for lora_name in args.enable_lora:
            if lora_name in loras:
                loras_to_load.append((lora_name, loras[lora_name]))
            else:
                print(f"Warning: LoRA '{lora_name}' not found in config")
    else:
        # Otherwise, load all enabled LoRAs from config
        loras_to_load = [(name, lora) for name, lora in loras.items() if lora.get("enabled", False)]

    for lora_name, lora_config in loras_to_load:
        lora_path = lora_config.get("path")
        lora_weight = lora_config.get("weight", 1.0)
        if lora_path and Path(lora_path).exists():
            print(f"Loading LoRA: {lora_name} ({lora_config.get('description', 'No description')})")
            generator.load_lora(lora_path, weight=lora_weight, adapter_name=lora_name)
        else:
            print(f"Warning: LoRA file not found: {lora_path}")

    # Generate images
    negative_prompt = args.negative_prompt if args.negative_prompt is not None else gen_defaults.get("negative_prompt", "")

    images = generator.generate(
        prompt=args.prompt,
        negative_prompt=negative_prompt,
        width=gen_defaults.get("width", 1024),
        height=gen_defaults.get("height", 1024),
        num_inference_steps=gen_defaults.get("num_inference_steps", 30),
        guidance_scale=gen_defaults.get("guidance_scale", 7.5),
        num_images=args.num_images,
        seed=args.seed,
        lora_scale=gen_defaults.get("lora_scale", 1.0),
        save_metadata=True
    )

    print(f"\n✓ Generated {len(images)} image(s) successfully!")


if __name__ == "__main__":
    main()
