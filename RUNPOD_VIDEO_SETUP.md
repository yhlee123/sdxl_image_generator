# RunPod Video Generation Setup Guide

## Prerequisites
- RunPod account with network storage set up
- RTX 5090 GPU pod (or similar high-end GPU)
- SSH access configured

## Step 1: Copy Video Generation Script to RunPod

From your local machine, you need to upload the video generation script to your RunPod instance.

### Option A: Using SCP (Secure Copy)
```bash
# Get your RunPod SSH connection details from the Connect tab
# Replace with your actual pod ID and connection details

scp /Users/younghoonmac/Projects/sdxl_image_generator_new/generate_video.py \
    root@<POD_ID>-<PORT>.runpod.io:/workspace/sdxl_image_generator/
```

### Option B: Manual Upload via RunPod Web Terminal
1. Go to RunPod.io → Your Pod → Connect → Web Terminal
2. Create the directory structure:
   ```bash
   cd /workspace
   mkdir -p sdxl_image_generator
   cd sdxl_image_generator
   ```
3. Create the file using nano or vim:
   ```bash
   nano generate_video.py
   ```
4. Copy-paste the script content from your local file

## Step 2: Install Required Dependencies on RunPod

SSH into your RunPod instance and run:

```bash
# Activate your Python environment (if using venv)
cd /workspace/sdxl_image_generator

# Install video generation dependencies
pip install torch torchvision diffusers transformers accelerate \
    safetensors Pillow opencv-python imageio imageio-ffmpeg

# Verify installations
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import diffusers; print(f'Diffusers: {diffusers.__version__}')"
```

## Step 3: Upload a Test Image

You need an input image to convert to video. Use one of your generated images:

```bash
# On your local machine - upload a test image
scp /Users/younghoonmac/Projects/sdxl_image_generator/outputs/generated_20251017_112626.png \
    root@<POD_ID>-<PORT>.runpod.io:/workspace/sdxl_image_generator/test_image.png
```

## Step 4: Test Video Generation

On RunPod, run the video generation script:

```bash
cd /workspace/sdxl_image_generator

# Basic test (fast - 14 frames, ~2 seconds)
python generate_video.py \
  --image test_image.png \
  --num-frames 14 \
  --fps 7 \
  --motion-bucket-id 127 \
  --device cuda \
  --dtype float16

# Full quality test (25 frames, ~4 seconds)
python generate_video.py \
  --image test_image.png \
  --num-frames 25 \
  --fps 6 \
  --motion-bucket-id 127 \
  --noise-aug-strength 0.02 \
  --device cuda \
  --dtype float16
```

### Motion Parameters Explained:
- **num-frames**: Total frames (14-25 recommended, more = longer video but slower)
- **fps**: Frames per second (6-8 recommended for smooth motion)
- **motion-bucket-id**: Amount of motion (1-255)
  - 50-100: Subtle motion (breathing, slight movements)
  - 127: Moderate motion (default, good for most content)
  - 150-200: Stronger motion (more dynamic)
- **noise-aug-strength**: Noise level (0.0-0.1)
  - 0.02: Default, good balance
  - Lower = more consistent but less dynamic
  - Higher = more variation but can be less coherent

## Step 5: Download Generated Video

```bash
# On your local machine
scp root@<POD_ID>-<PORT>.runpod.io:/workspace/sdxl_image_generator/outputs/video_*.mp4 \
    /Users/younghoonmac/Projects/sdxl_image_generator/outputs/
```

## Step 6: Benchmark Different Settings

Test with different motion settings to find what works best for your content:

```bash
# Subtle motion (good for portrait/glamour shots)
python generate_video.py --image test_image.png --motion-bucket-id 80 --num-frames 14

# Moderate motion (default)
python generate_video.py --image test_image.png --motion-bucket-id 127 --num-frames 25

# Strong motion (more dynamic, may introduce artifacts)
python generate_video.py --image test_image.png --motion-bucket-id 180 --num-frames 25
```

## Troubleshooting

### Out of Memory Error
```bash
# Reduce decode chunk size
python generate_video.py --image test_image.png --decode-chunk-size 4

# Or reduce number of frames
python generate_video.py --image test_image.png --num-frames 14
```

### Slow Generation
- This is normal! SVD is computationally intensive
- 25 frames can take 3-5 minutes on RTX 5090
- 14 frames takes about 2-3 minutes

### Poor Video Quality
- Ensure input image is high quality (768x1024 or 1024x1024)
- Try different motion_bucket_id values
- Adjust noise_aug_strength (try 0.01 or 0.03)

## Performance Estimates (RTX 5090)

| Frames | FPS | Duration | Generation Time | Cost (RunPod) |
|--------|-----|----------|-----------------|---------------|
| 14     | 7   | ~2 sec   | ~2-3 min        | ~$0.02        |
| 25     | 6   | ~4 sec   | ~4-5 min        | ~$0.04        |
| 50     | 8   | ~6 sec   | ~8-10 min       | ~$0.08        |

*Note: Costs assume $0.89/hr RunPod pricing*

## Next Steps After Testing

1. ✅ Verify video quality meets your standards
2. ✅ Document best motion parameters for different content types
3. ✅ Test batch processing (multiple images → multiple videos)
4. ✅ Set up automated pipeline for production

## Production Optimization Tips

1. **Batch Processing**: Generate multiple videos in one session to amortize model loading time
2. **Motion Presets**: Create presets for different character types
   - Portrait/glamour: motion_bucket_id=80-100
   - Dynamic/action: motion_bucket_id=150-180
3. **Resolution**: Input images at 768x1024 work well (will be resized to 1024x576)
4. **Frame Count**: 14-25 frames is sweet spot for quality vs. speed

## Example Production Script

```python
# batch_video_gen.py
import glob
from generate_video import VideoGenerator

# Initialize once (saves time)
gen = VideoGenerator(device="cuda", dtype="float16")

# Process all images
for img_path in glob.glob("outputs/*.png"):
    print(f"Processing {img_path}...")
    gen.generate_video(
        image_path=img_path,
        num_frames=25,
        motion_bucket_id=127
    )
```
