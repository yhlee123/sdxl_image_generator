#!/usr/bin/env python3
"""
Complete Image-to-Video Workflow
Generates an image using SDXL + LoRA, then creates a video from it using SVD
"""

import argparse
import os
import sys
from pathlib import Path

# Import our generators
from generate import SDXLGenerator
from generate_video import VideoGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Complete workflow: Generate image with SDXL + LoRA, then create video"
    )

    # Image generation arguments
    img_group = parser.add_argument_group('Image Generation')
    img_group.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Text prompt for image generation"
    )
    img_group.add_argument(
        "--negative-prompt",
        type=str,
        default="low quality, blurry, watermark",
        help="Negative prompt"
    )
    img_group.add_argument(
        "--lora",
        type=str,
        action="append",
        default=[],
        help="Path to LoRA file (can specify multiple)"
    )
    img_group.add_argument(
        "--lora-scale",
        type=float,
        default=0.8,
        help="LoRA scale/weight"
    )
    img_group.add_argument(
        "--image-steps",
        type=int,
        default=30,
        help="Inference steps for image generation"
    )

    # Video generation arguments
    vid_group = parser.add_argument_group('Video Generation')
    vid_group.add_argument(
        "--num-frames",
        type=int,
        default=25,
        help="Number of frames (25 frames = ~4 seconds at 6fps)"
    )
    vid_group.add_argument(
        "--fps",
        type=int,
        default=6,
        help="Frames per second"
    )
    vid_group.add_argument(
        "--motion",
        type=int,
        default=127,
        help="Motion amount (1-255, higher = more motion)"
    )

    # Common arguments
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        choices=["cuda", "mps", "cpu"],
        help="Device to use"
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
        help="Output directory"
    )
    parser.add_argument(
        "--skip-image",
        type=str,
        default=None,
        help="Skip image generation and use existing image (path)"
    )

    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("SDXL Image-to-Video Workflow")
    print("=" * 60)
    print()

    # Step 1: Generate or load image
    if args.skip_image:
        print("Step 1: Using existing image")
        print(f"Image: {args.skip_image}")
        image_path = args.skip_image
        if not os.path.exists(image_path):
            print(f"Error: Image not found: {image_path}")
            sys.exit(1)
    else:
        print("Step 1: Generating image with SDXL + LoRA")
        print("-" * 60)

        # Create image generator
        img_generator = SDXLGenerator(
            model_id="stabilityai/stable-diffusion-xl-base-1.0",
            device=args.device,
            dtype="float16",
            output_dir=args.output_dir
        )

        # Load LoRAs
        for lora_path in args.lora:
            if os.path.exists(lora_path):
                img_generator.load_lora(lora_path, weight=args.lora_scale)
            else:
                print(f"Warning: LoRA not found: {lora_path}")

        # Generate image
        images = img_generator.generate(
            prompt=args.prompt,
            negative_prompt=args.negative_prompt,
            width=1024,
            height=576,  # SVD optimal resolution
            num_inference_steps=args.image_steps,
            guidance_scale=7.5,
            num_images=1,
            seed=args.seed,
            lora_scale=args.lora_scale,
            save_metadata=True
        )

        # Get the path of generated image
        # Find the most recent image in output directory
        image_files = sorted(output_dir.glob("generated_*.png"), key=os.path.getmtime)
        if not image_files:
            print("Error: Image generation failed")
            sys.exit(1)
        image_path = str(image_files[-1])
        print(f"\n✓ Image generated: {image_path}")

    print()
    print("Step 2: Generating video from image")
    print("-" * 60)

    # Create video generator
    vid_generator = VideoGenerator(
        model_id="stabilityai/stable-video-diffusion-img2vid-xt",
        device=args.device,
        dtype="float16",
        output_dir=args.output_dir
    )

    # Generate video
    video_path = vid_generator.generate_video(
        image_path=image_path,
        num_frames=args.num_frames,
        fps=args.fps,
        motion_bucket_id=args.motion,
        noise_aug_strength=0.02,
        decode_chunk_size=8,
        seed=args.seed,
        save_metadata=True
    )

    print()
    print("=" * 60)
    print("✓ Workflow Complete!")
    print("=" * 60)
    print(f"Input image: {image_path}")
    print(f"Output video: {video_path}")
    print(f"Duration: {args.num_frames / args.fps:.1f} seconds")
    print()
    print(f"To view video: open '{video_path}'")
    print()


if __name__ == "__main__":
    main()
