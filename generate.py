#!/usr/bin/env python3
"""
SDXL Image Generator with LoRA Support
A general-purpose tool for generating images using Stable Diffusion XL and LoRA models.
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict

import torch
from diffusers import StableDiffusionXLPipeline, AutoencoderKL
from diffusers.utils import load_image
from safetensors.torch import load_file
from PIL import Image, PngImagePlugin


class SDXLGenerator:
    """SDXL image generator with LoRA support."""

    def __init__(
        self,
        model_id: str = "stabilityai/stable-diffusion-xl-base-1.0",
        vae_model: Optional[str] = None,
        device: str = "mps",
        dtype: str = "float16",
        output_dir: str = "./outputs"
    ):
        """
        Initialize the SDXL generator.

        Args:
            model_id: HuggingFace model ID or local path
            vae_model: Optional separate VAE model
            device: Device to run on (mps for Mac, cuda for NVIDIA, cpu)
            dtype: Data type (float16 or float32)
            output_dir: Directory to save generated images
        """
        self.model_id = model_id
        self.device = device
        self.dtype = torch.float16 if dtype == "float16" else torch.float32
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        print(f"Loading model: {model_id}")
        print(f"Device: {device}, dtype: {dtype}")

        # Load VAE if specified
        vae = None
        if vae_model:
            print(f"Loading VAE: {vae_model}")
            vae = AutoencoderKL.from_pretrained(vae_model, torch_dtype=self.dtype)

        # Load the pipeline
        self.pipe = StableDiffusionXLPipeline.from_pretrained(
            model_id,
            vae=vae,
            torch_dtype=self.dtype,
            use_safetensors=True,
        )

        # Move to device
        if device == "mps":
            self.pipe = self.pipe.to("mps")
            # Enable attention slicing for better memory efficiency on Mac
            self.pipe.enable_attention_slicing()
        elif device == "cuda":
            self.pipe = self.pipe.to("cuda")
        else:
            self.pipe = self.pipe.to("cpu")

        print("Model loaded successfully!")

        self.loaded_loras: List[Dict] = []

    def load_lora(self, lora_path: str, weight: float = 1.0, adapter_name: Optional[str] = None):
        """
        Load a LoRA model.

        Args:
            lora_path: Path to the LoRA safetensors file
            weight: Weight/strength of the LoRA (0.0 to 2.0, typically)
            adapter_name: Optional name for this LoRA adapter
        """
        if not os.path.exists(lora_path):
            print(f"Warning: LoRA file not found: {lora_path}")
            return

        lora_name = adapter_name or Path(lora_path).stem
        print(f"Loading LoRA: {lora_name} with weight {weight}")

        try:
            self.pipe.load_lora_weights(lora_path, adapter_name=lora_name)
            self.loaded_loras.append({
                "name": lora_name,
                "path": lora_path,
                "weight": weight
            })
            print(f"LoRA '{lora_name}' loaded successfully!")
        except Exception as e:
            print(f"Error loading LoRA: {e}")

    def set_lora_scale(self, weight: float):
        """Set the scale for all loaded LoRAs."""
        if self.loaded_loras:
            self.pipe.set_adapters(
                [lora["name"] for lora in self.loaded_loras],
                adapter_weights=[weight] * len(self.loaded_loras)
            )

    def unload_loras(self):
        """Unload all LoRAs."""
        if self.loaded_loras:
            print("Unloading LoRAs...")
            self.pipe.unload_lora_weights()
            self.loaded_loras = []

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        num_images: int = 1,
        seed: Optional[int] = None,
        lora_scale: float = 1.0,
        save_metadata: bool = True
    ) -> List[Image.Image]:
        """
        Generate images.

        Args:
            prompt: Text prompt for generation
            negative_prompt: Negative prompt
            width: Image width (must be multiple of 8)
            height: Image height (must be multiple of 8)
            num_inference_steps: Number of denoising steps
            guidance_scale: How closely to follow the prompt (1.0-20.0)
            num_images: Number of images to generate
            seed: Random seed for reproducibility
            lora_scale: Scale/weight for LoRAs
            save_metadata: Whether to save generation metadata

        Returns:
            List of generated PIL Images
        """
        # Set LoRA scale if any LoRAs are loaded
        if self.loaded_loras and lora_scale != 1.0:
            self.set_lora_scale(lora_scale)

        # Set seed if specified
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)

        print("\nGenerating images...")
        print(f"Prompt: {prompt}")
        print(f"Size: {width}x{height}")
        print(f"Steps: {num_inference_steps}, Guidance: {guidance_scale}")
        if self.loaded_loras:
            print(f"LoRAs: {', '.join([l['name'] for l in self.loaded_loras])} (scale: {lora_scale})")

        # Generate images
        images = []
        for i in range(num_images):
            if num_images > 1:
                print(f"Generating image {i+1}/{num_images}...")

            result = self.pipe(
                prompt=prompt,
                negative_prompt=negative_prompt if negative_prompt else None,
                width=width,
                height=height,
                num_inference_steps=num_inference_steps,
                guidance_scale=guidance_scale,
                generator=generator,
            )

            image = result.images[0]

            # Save image with metadata
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_{timestamp}_{i+1}.png" if num_images > 1 else f"generated_{timestamp}.png"
            filepath = self.output_dir / filename

            if save_metadata:
                # Add metadata to PNG
                metadata = PngImagePlugin.PngInfo()
                metadata.add_text("prompt", prompt)
                metadata.add_text("negative_prompt", negative_prompt)
                metadata.add_text("width", str(width))
                metadata.add_text("height", str(height))
                metadata.add_text("steps", str(num_inference_steps))
                metadata.add_text("guidance_scale", str(guidance_scale))
                metadata.add_text("seed", str(seed) if seed is not None else "random")
                metadata.add_text("model", self.model_id)
                if self.loaded_loras:
                    metadata.add_text("loras", json.dumps(self.loaded_loras))
                    metadata.add_text("lora_scale", str(lora_scale))

                image.save(filepath, pnginfo=metadata)
            else:
                image.save(filepath)

            print(f"Saved: {filepath}")
            images.append(image)

        return images


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Stable Diffusion XL with LoRA support"
    )

    # Model arguments
    parser.add_argument(
        "--model",
        type=str,
        default="stabilityai/stable-diffusion-xl-base-1.0",
        help="Model ID or path"
    )
    parser.add_argument(
        "--vae",
        type=str,
        default=None,
        help="Optional VAE model path"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="mps",
        choices=["mps", "cuda", "cpu"],
        help="Device to use (mps for Mac, cuda for NVIDIA GPU, cpu)"
    )
    parser.add_argument(
        "--dtype",
        type=str,
        default="float16",
        choices=["float16", "float32"],
        help="Data type for model weights"
    )

    # LoRA arguments
    parser.add_argument(
        "--lora",
        type=str,
        action="append",
        default=[],
        help="Path to LoRA file (can specify multiple times)"
    )
    parser.add_argument(
        "--lora-scale",
        type=float,
        default=1.0,
        help="LoRA scale/weight (0.0-2.0)"
    )

    # Generation arguments
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Text prompt for image generation"
    )
    parser.add_argument(
        "--negative-prompt",
        type=str,
        default="",
        help="Negative prompt"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=1024,
        help="Image width (must be multiple of 8)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=1024,
        help="Image height (must be multiple of 8)"
    )
    parser.add_argument(
        "--steps",
        type=int,
        default=30,
        help="Number of inference steps"
    )
    parser.add_argument(
        "--guidance-scale",
        type=float,
        default=7.5,
        help="Guidance scale (how closely to follow prompt)"
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

    # Output arguments
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./outputs",
        help="Directory to save generated images"
    )
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Don't save generation metadata in images"
    )

    args = parser.parse_args()

    # Create generator
    generator = SDXLGenerator(
        model_id=args.model,
        vae_model=args.vae,
        device=args.device,
        dtype=args.dtype,
        output_dir=args.output_dir
    )

    # Load LoRAs
    for lora_path in args.lora:
        generator.load_lora(lora_path, weight=args.lora_scale)

    # Generate images
    images = generator.generate(
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        width=args.width,
        height=args.height,
        num_inference_steps=args.steps,
        guidance_scale=args.guidance_scale,
        num_images=args.num_images,
        seed=args.seed,
        lora_scale=args.lora_scale,
        save_metadata=not args.no_metadata
    )

    print(f"\n✓ Generated {len(images)} image(s) successfully!")


if __name__ == "__main__":
    main()
