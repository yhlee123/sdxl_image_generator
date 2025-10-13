#!/usr/bin/env python3
"""
Cost Monitoring and Management for RunPod
Tracks usage time and estimates costs
"""

import argparse
import json
from datetime import datetime, timedelta
from pathlib import Path


class CostMonitor:
    """Monitor and estimate RunPod costs."""

    # Common GPU pricing (per hour) - Update these based on current RunPod rates
    GPU_PRICES = {
        "RTX 3090": 0.44,
        "RTX 4090": 0.69,
        "RTX A6000": 0.79,
        "A100 40GB": 1.39,
        "A100 80GB": 1.89,
        "H100": 3.99,
    }

    def __init__(self, log_file: str = "./runpod/usage_log.json"):
        self.log_file = Path(log_file)
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.sessions = self.load_log()

    def load_log(self):
        """Load usage log from file."""
        if self.log_file.exists():
            with open(self.log_file, 'r') as f:
                return json.load(f)
        return {"sessions": []}

    def save_log(self):
        """Save usage log to file."""
        with open(self.log_file, 'w') as f:
            json.dump(self.sessions, f, indent=2)

    def start_session(self, gpu_type: str, pod_id: str = None):
        """Start a new usage session."""
        session = {
            "pod_id": pod_id or "unknown",
            "gpu_type": gpu_type,
            "start_time": datetime.now().isoformat(),
            "end_time": None,
            "duration_hours": 0,
            "estimated_cost": 0
        }
        self.sessions["sessions"].append(session)
        self.save_log()

        print(f"✓ Session started: {gpu_type}")
        print(f"  Pod ID: {pod_id}")
        print(f"  Hourly rate: ${self.GPU_PRICES.get(gpu_type, 0):.2f}/hour")
        return len(self.sessions["sessions"]) - 1

    def end_session(self, session_index: int = -1):
        """End a usage session."""
        if not self.sessions["sessions"]:
            print("No active sessions")
            return

        session = self.sessions["sessions"][session_index]
        if session["end_time"]:
            print("Session already ended")
            return

        start = datetime.fromisoformat(session["start_time"])
        end = datetime.now()
        duration = (end - start).total_seconds() / 3600  # Convert to hours

        session["end_time"] = end.isoformat()
        session["duration_hours"] = round(duration, 3)
        session["estimated_cost"] = round(
            duration * self.GPU_PRICES.get(session["gpu_type"], 0),
            2
        )

        self.save_log()

        print(f"\n✓ Session ended")
        print(f"  GPU: {session['gpu_type']}")
        print(f"  Duration: {duration:.2f} hours ({int(duration * 60)} minutes)")
        print(f"  Estimated cost: ${session['estimated_cost']:.2f}")

    def estimate_cost(self, gpu_type: str, hours: float):
        """Estimate cost for given GPU and hours."""
        rate = self.GPU_PRICES.get(gpu_type, 0)
        cost = hours * rate
        return cost

    def estimate_for_workflow(
        self,
        gpu_type: str,
        num_images: int = 0,
        num_videos: int = 0,
        time_per_image: float = 30,  # seconds
        time_per_video: float = 120,  # seconds
    ):
        """Estimate cost for a specific workflow."""
        total_time_seconds = (num_images * time_per_image) + (num_videos * time_per_video)
        total_hours = total_time_seconds / 3600
        cost = self.estimate_cost(gpu_type, total_hours)

        print("\n" + "=" * 60)
        print("COST ESTIMATION")
        print("=" * 60)
        print(f"GPU: {gpu_type} (${self.GPU_PRICES.get(gpu_type, 0):.2f}/hour)")
        print(f"\nWorkload:")
        print(f"  Images: {num_images} ({time_per_image}s each)")
        print(f"  Videos: {num_videos} ({time_per_video}s each)")
        print(f"\nEstimated time: {total_hours:.2f} hours ({int(total_time_seconds / 60)} minutes)")
        print(f"Estimated cost: ${cost:.2f}")
        print("=" * 60)

        return cost

    def get_summary(self):
        """Get usage summary."""
        if not self.sessions["sessions"]:
            print("No usage sessions recorded")
            return

        total_cost = sum(s["estimated_cost"] for s in self.sessions["sessions"])
        total_hours = sum(s["duration_hours"] for s in self.sessions["sessions"])
        active_sessions = sum(1 for s in self.sessions["sessions"] if not s["end_time"])

        print("\n" + "=" * 60)
        print("USAGE SUMMARY")
        print("=" * 60)
        print(f"Total sessions: {len(self.sessions['sessions'])}")
        print(f"Active sessions: {active_sessions}")
        print(f"Total runtime: {total_hours:.2f} hours")
        print(f"Total cost: ${total_cost:.2f}")
        print("=" * 60)

        # Show recent sessions
        print("\nRecent sessions:")
        for session in self.sessions["sessions"][-5:]:
            start = datetime.fromisoformat(session["start_time"])
            status = "ACTIVE" if not session["end_time"] else "ENDED"
            print(f"  [{status}] {session['gpu_type']} - {start.strftime('%Y-%m-%d %H:%M')} - ${session['estimated_cost']:.2f}")

    def list_gpu_prices(self):
        """List available GPU types and prices."""
        print("\n" + "=" * 60)
        print("GPU PRICING (per hour)")
        print("=" * 60)
        for gpu, price in sorted(self.GPU_PRICES.items(), key=lambda x: x[1]):
            print(f"  {gpu:20s} ${price:.2f}/hour")
        print("=" * 60)
        print("\nNote: Prices may vary. Check RunPod for current rates.")


def main():
    parser = argparse.ArgumentParser(
        description="Monitor and estimate RunPod costs"
    )

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Start session
    start_parser = subparsers.add_parser('start', help='Start a usage session')
    start_parser.add_argument('--gpu', type=str, required=True, help='GPU type')
    start_parser.add_argument('--pod-id', type=str, default=None, help='Pod ID')

    # End session
    subparsers.add_parser('end', help='End current session')

    # Estimate
    estimate_parser = subparsers.add_parser('estimate', help='Estimate costs')
    estimate_parser.add_argument('--gpu', type=str, required=True, help='GPU type')
    estimate_parser.add_argument('--images', type=int, default=0, help='Number of images')
    estimate_parser.add_argument('--videos', type=int, default=0, help='Number of videos')
    estimate_parser.add_argument('--time-per-image', type=float, default=30, help='Seconds per image')
    estimate_parser.add_argument('--time-per-video', type=float, default=120, help='Seconds per video')

    # Summary
    subparsers.add_parser('summary', help='Show usage summary')

    # List prices
    subparsers.add_parser('prices', help='List GPU prices')

    args = parser.parse_args()

    monitor = CostMonitor()

    if args.command == 'start':
        monitor.start_session(args.gpu, args.pod_id)
    elif args.command == 'end':
        monitor.end_session()
    elif args.command == 'estimate':
        monitor.estimate_for_workflow(
            args.gpu,
            args.images,
            args.videos,
            args.time_per_image,
            args.time_per_video
        )
    elif args.command == 'summary':
        monitor.get_summary()
    elif args.command == 'prices':
        monitor.list_gpu_prices()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
