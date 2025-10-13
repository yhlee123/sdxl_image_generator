#!/usr/bin/env python3
"""
Performance Benchmark Script for RunPod
Tests image and video generation performance on cloud GPU
"""

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
import sys

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from generate import SDXLGenerator
from generate_video import VideoGenerator


class PerformanceBenchmark:
    """Benchmark image and video generation performance."""

    def __init__(self, output_dir: str = "./benchmark_results"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }

    def benchmark_image_generation(
        self,
        device: str = "cuda",
        test_prompts: list = None,
        lora_path: str = None
    ):
        """Benchmark SDXL image generation."""
        if test_prompts is None:
            test_prompts = [
                "a beautiful landscape with mountains and lake",
                "portrait of a person in professional attire",
                "abstract art with vibrant colors"
            ]

        print("\n" + "=" * 60)
        print("BENCHMARKING IMAGE GENERATION")
        print("=" * 60)

        generator = SDXLGenerator(
            device=device,
            dtype="float16",
            output_dir=str(self.output_dir)
        )

        if lora_path:
            print(f"Loading LoRA: {lora_path}")
            generator.load_lora(lora_path, weight=0.8)

        for idx, prompt in enumerate(test_prompts, 1):
            print(f"\nTest {idx}/{len(test_prompts)}: {prompt[:50]}...")

            start_time = time.time()
            images = generator.generate(
                prompt=prompt,
                width=1024,
                height=1024,
                num_inference_steps=30,
                guidance_scale=7.5,
                num_images=1,
                save_metadata=False
            )
            elapsed = time.time() - start_time

            result = {
                "type": "image_generation",
                "test_number": idx,
                "prompt": prompt,
                "resolution": "1024x1024",
                "steps": 30,
                "time_seconds": round(elapsed, 2),
                "lora_used": lora_path is not None
            }

            self.results["tests"].append(result)
            print(f"✓ Completed in {elapsed:.2f} seconds")

        avg_time = sum(t["time_seconds"] for t in self.results["tests"]
                      if t["type"] == "image_generation") / len(test_prompts)
        print(f"\nAverage time per image: {avg_time:.2f} seconds")

    def benchmark_video_generation(
        self,
        device: str = "cuda",
        test_image: str = None,
        frame_counts: list = None
    ):
        """Benchmark SVD video generation."""
        if frame_counts is None:
            frame_counts = [14, 25]  # Short and medium length videos

        print("\n" + "=" * 60)
        print("BENCHMARKING VIDEO GENERATION")
        print("=" * 60)

        # Use test image or generate one
        if test_image is None or not Path(test_image).exists():
            print("\nGenerating test image for video benchmark...")
            img_gen = SDXLGenerator(
                device=device,
                dtype="float16",
                output_dir=str(self.output_dir)
            )
            img_gen.generate(
                prompt="a scenic landscape, professional photography",
                width=1024,
                height=576,
                num_inference_steps=25,
                save_metadata=False
            )
            # Get most recent image
            images = sorted(self.output_dir.glob("generated_*.png"), key=lambda p: p.stat().st_mtime)
            test_image = str(images[-1])
            print(f"Using test image: {test_image}")

        vid_gen = VideoGenerator(
            device=device,
            dtype="float16",
            output_dir=str(self.output_dir)
        )

        for idx, num_frames in enumerate(frame_counts, 1):
            duration = num_frames / 6  # Assuming 6 fps
            print(f"\nTest {idx}/{len(frame_counts)}: {num_frames} frames (~{duration:.1f}s)")

            start_time = time.time()
            video_path = vid_gen.generate_video(
                image_path=test_image,
                num_frames=num_frames,
                fps=6,
                save_metadata=False
            )
            elapsed = time.time() - start_time

            result = {
                "type": "video_generation",
                "test_number": idx,
                "num_frames": num_frames,
                "duration_seconds": round(duration, 1),
                "time_seconds": round(elapsed, 2),
                "fps": 6
            }

            self.results["tests"].append(result)
            print(f"✓ Completed in {elapsed:.2f} seconds")

        avg_time = sum(t["time_seconds"] for t in self.results["tests"]
                      if t["type"] == "video_generation") / len(frame_counts)
        print(f"\nAverage time per video: {avg_time:.2f} seconds")

    def save_results(self):
        """Save benchmark results to JSON."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = self.output_dir / f"benchmark_{timestamp}.json"

        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)

        print(f"\n✓ Results saved to: {results_file}")
        return results_file

    def print_summary(self):
        """Print benchmark summary."""
        print("\n" + "=" * 60)
        print("BENCHMARK SUMMARY")
        print("=" * 60)

        image_tests = [t for t in self.results["tests"] if t["type"] == "image_generation"]
        video_tests = [t for t in self.results["tests"] if t["type"] == "video_generation"]

        if image_tests:
            avg_img_time = sum(t["time_seconds"] for t in image_tests) / len(image_tests)
            print(f"\nImage Generation:")
            print(f"  Tests: {len(image_tests)}")
            print(f"  Average: {avg_img_time:.2f}s per image")
            print(f"  Range: {min(t['time_seconds'] for t in image_tests):.2f}s - {max(t['time_seconds'] for t in image_tests):.2f}s")

        if video_tests:
            avg_vid_time = sum(t["time_seconds"] for t in video_tests) / len(video_tests)
            print(f"\nVideo Generation:")
            print(f"  Tests: {len(video_tests)}")
            print(f"  Average: {avg_vid_time:.2f}s per video")
            print(f"  Range: {min(t['time_seconds'] for t in video_tests):.2f}s - {max(t['time_seconds'] for t in video_tests):.2f}s")

        print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Benchmark performance on RunPod GPU"
    )

    parser.add_argument(
        "--device",
        type=str,
        default="cuda",
        choices=["cuda", "mps", "cpu"],
        help="Device to benchmark"
    )
    parser.add_argument(
        "--test-image",
        action="store_true",
        help="Run image generation benchmarks"
    )
    parser.add_argument(
        "--test-video",
        action="store_true",
        help="Run video generation benchmarks"
    )
    parser.add_argument(
        "--test-all",
        action="store_true",
        help="Run all benchmarks"
    )
    parser.add_argument(
        "--lora",
        type=str,
        default=None,
        help="Path to LoRA for image testing"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./benchmark_results",
        help="Output directory for results"
    )

    args = parser.parse_args()

    # Default to all tests if none specified
    if not (args.test_image or args.test_video or args.test_all):
        args.test_all = True

    benchmark = PerformanceBenchmark(output_dir=args.output_dir)

    try:
        if args.test_all or args.test_image:
            benchmark.benchmark_image_generation(
                device=args.device,
                lora_path=args.lora
            )

        if args.test_all or args.test_video:
            benchmark.benchmark_video_generation(
                device=args.device
            )

        benchmark.print_summary()
        benchmark.save_results()

    except KeyboardInterrupt:
        print("\n\nBenchmark interrupted by user")
        benchmark.save_results()
    except Exception as e:
        print(f"\nError during benchmark: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
