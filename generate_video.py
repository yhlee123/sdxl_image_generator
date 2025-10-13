#!/usr/bin/env python3
"""
SDXL Video Generator using Stable Video Diffusion
Generates videos from images using SVD (img2vid pipeline)
"""

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

import torch
from diffusers import StableVideoDiffusionPipeline
from diffusers.utils import load_image, export_to_video
from PIL import Image


class VideoGenerator:
    """Video generator using Stable Video Diffusion."""

    def __init__(
        self,
        model_id: str = "stabilityai/stable-video-diffusion-img2vid-xt",
        device: str = "cuda",
        dtype: str = "float16",
        output_dir: str = "./outputs"
    ):
        """
        Initialize the video generator.

        Args:
            model_id: HuggingFace model ID or local path for SVD
            device: Device to run on (cuda for GPU, mps for Mac, cpu)
            dtype: Data type (float16 or float32)
            output_dir: Directory to save generated videos
        """
        self.model_id = model_id
        self.device = device
        self.dtype = torch.float16 if dtype == "float16" else torch.float32
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        print(f"Loading video generation model: {model_id}")
        print(f"Device: {device}, dtype: {dtype}")
        print("This may take a few minutes on first run...")

        # Load the SVD pipeline
        self.pipe = StableVideoDiffusionPipeline.from_pretrained(
            model_id,
            torch_dtype=self.dtype,
            variant="fp16" if dtype == "float16" else None,
        )

        # Move to device
        if device == "cuda":
            self.pipe = self.pipe.to("cuda")
            # Enable memory efficient attention
            self.pipe.enable_model_cpu_offload()
        elif device == "mps":
            # Mac Metal support (if available)
            self.pipe = self.pipe.to("mps")
        else:
            self.pipe = self.pipe.to("cpu")

        print("Video generation model loaded successfully!")

    def generate_video(
        self,
        image_path: str,
        num_frames: int = 25,
        fps: int = 6,
        motion_bucket_id: int = 127,
        noise_aug_strength: float = 0.02,
        decode_chunk_size: int = 8,
        seed: Optional[int] = None,
        save_metadata: bool = True
    ) -> str:
        """
        Generate a video from an input image.

        Args:
            image_path: Path to input image
            num_frames: Number of frames to generate (default: 25, ~4 seconds at 6fps)
            fps: Frames per second for output video
            motion_bucket_id: Controls amount of motion (higher = more motion, 1-255)
            noise_aug_strength: Noise augmentation strength (0.0-1.0)
            decode_chunk_size: Chunk size for decoding (lower = less VRAM)
            seed: Random seed for reproducibility
            save_metadata: Whether to save generation metadata

        Returns:
            Path to generated video file
        """
        # Load and preprocess image
        print(f"\nLoading image: {image_path}")
        image = load_image(image_path)

        # Resize image to supported resolution (1024x576 for SVD-XT)
        image = image.resize((1024, 576))

        # Set seed if specified
        generator = None
        if seed is not None:
            generator = torch.Generator(device=self.device).manual_seed(seed)

        print(f"\nGenerating video...")
        print(f"Frames: {num_frames} ({num_frames/fps:.1f} seconds at {fps} fps)")
        print(f"Motion: {motion_bucket_id}, Noise: {noise_aug_strength}")

        # Generate video frames
        frames = self.pipe(
            image,
            num_frames=num_frames,
            motion_bucket_id=motion_bucket_id,
            noise_aug_strength=noise_aug_strength,
            decode_chunk_size=decode_chunk_size,
            generator=generator,
        ).frames[0]

        # Save video
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_filename = f"video_{timestamp}.mp4"
        video_path = self.output_dir / video_filename

        print(f"\nExporting video to: {video_path}")
        export_to_video(frames, str(video_path), fps=fps)

        # Save metadata if requested
        if save_metadata:
            metadata = {
                "input_image": str(image_path),
                "num_frames": num_frames,
                "fps": fps,
                "duration_seconds": num_frames / fps,
                "motion_bucket_id": motion_bucket_id,
                "noise_aug_strength": noise_aug_strength,
                "seed": seed,
                "model": self.model_id,
                "timestamp": timestamp
            }

            metadata_path = self.output_dir / f"video_{timestamp}_metadata.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            print(f"Metadata saved to: {metadata_path}")

        print(f"\n✓ Video generation complete!")
        print(f"Duration: {num_frames/fps:.1f} seconds")
        print(f"Resolution: 1024x576")

        return str(video_path)


def main():
    parser = argparse.ArgumentParser(
        description="Generate videos from images using Stable Video Diffusion"
    )

    # Model arguments
    parser.add_argument(
        "--model",
        type=str,
        default="stabilityai/stable-video-diffusion-img2vid-xt",
        help="SVD model ID or path"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        choices=["cuda", "mps", "cpu"],
        help="Device to use"
    )
    parser.add_argument(
        "--dtype",
        type=str,
        default="float16",
        choices=["float16", "float32"],
        help="Data type for model weights"
    )

    # Input/Output
    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="Path to input image"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./outputs",
        help="Directory to save generated videos"
    )

    # Generation parameters
    parser.add_argument(
        "--num-frames",
        type=int,
        default=25,
        help="Number of frames to generate (default: 25, ~4 seconds at 6fps)"
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=6,
        help="Frames per second for output video"
    )
    parser.add_argument(
        "--motion-bucket-id",
        type=int,
        default=127,
        help="Controls amount of motion (1-255, higher = more motion)"
    )
    parser.add_argument(
        "--noise-aug-strength",
        type=float,
        default=0.02,
        help="Noise augmentation strength (0.0-1.0)"
    )
    parser.add_argument(
        "--decode-chunk-size",
        type=int,
        default=8,
        help="Chunk size for decoding (lower = less VRAM)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        "--no-metadata",
        action="store_true",
        help="Don't save generation metadata"
    )

    args = parser.parse_args()

    # Validate input image exists
    if not os.path.exists(args.image):
        print(f"Error: Input image not found: {args.image}")
        return

    # Create generator
    generator = VideoGenerator(
        model_id=args.model,
        device=args.device,
        dtype=args.dtype,
        output_dir=args.output_dir
    )

    # Generate video
    video_path = generator.generate_video(
        image_path=args.image,
        num_frames=args.num_frames,
        fps=args.fps,
        motion_bucket_id=args.motion_bucket_id,
        noise_aug_strength=args.noise_aug_strength,
        decode_chunk_size=args.decode_chunk_size,
        seed=args.seed,
        save_metadata=not args.no_metadata
    )

    print(f"\nVideo saved to: {video_path}")
    print(f"To view: open '{video_path}'")


if __name__ == "__main__":
    main()
