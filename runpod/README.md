# RunPod Cloud GPU Setup Guide

Complete guide for deploying and using SDXL Image & Video Generator on RunPod cloud GPUs.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Step 1: RunPod Setup](#step-1-runpod-setup)
3. [Step 2: SSH Configuration](#step-2-ssh-configuration)
4. [Step 3: Deploy to RunPod](#step-3-deploy-to-runpod)
5. [Step 4: Running Generation](#step-4-running-generation)
6. [Step 5: Cost Management](#step-5-cost-management)
7. [Performance Benchmarking](#performance-benchmarking)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

- RunPod account with credits
- SSH key generated (done automatically by deploy script)
- Local copy of this repository

---

## Step 1: RunPod Setup

### 1.1 Create a Pod

1. Go to [RunPod.io](https://runpod.io) and sign in
2. Click "Deploy" → "Pods"
3. Choose GPU:
   - **Minimum**: RTX 3090 (24GB VRAM) - $0.44/hour
   - **Recommended**: RTX 4090 (24GB VRAM) - $0.69/hour
   - **Best**: A100 40GB - $1.39/hour

4. Select template:
   - Choose "PyTorch" or "RunPod Pytorch" template
   - This provides Python 3 and CUDA pre-installed

5. Configure:
   - **Volume**: Add 50GB+ persistent volume (optional but recommended)
   - **Network**: Enable SSH (port 22)
   - **Billing**: Choose "On-Demand"

6. Click "Deploy On-Demand"

### 1.2 Note Your Pod Details

After deployment, note these details (update `runpod/runpod_config.json`):
- **Pod ID**: Found in pod details
- **Pod Name**: Your pod's name
- **SSH Host**: The IP address (e.g., 213.181.111.2)
- **SSH Port**: The port number (e.g., 45425)

---

## Step 2: SSH Configuration

### 2.1 Add Your SSH Public Key to RunPod

Your SSH key has been generated at: `~/.ssh/runpod_key`

View your public key:
```bash
cat ~/.ssh/runpod_key.pub
```

Copy the output (starts with `ssh-ed25519`), then:

1. In RunPod console, click on your pod
2. Go to "Connect" tab
3. Find "SSH Public Key" section
4. Paste your public key
5. Click "Save"

### 2.2 Update Configuration

Edit `runpod/runpod_config.json` with your pod details:

```json
{
  "pod": {
    "id": "YOUR_POD_ID",
    "name": "YOUR_POD_NAME",
    "ssh_host": "YOUR_SSH_HOST",
    "ssh_port": YOUR_SSH_PORT,
    "ssh_user": "root",
    "ssh_key_path": "~/.ssh/runpod_key"
  }
}
```

### 2.3 Test Connection

```bash
./runpod/connect.sh
```

If successful, you'll be connected to your RunPod instance!

---

## Step 3: Deploy to RunPod

### 3.1 Deploy Code

Deploy the project to your RunPod instance:

```bash
./runpod/deploy.sh
```

This will:
- ✓ Sync all project files to RunPod
- ✓ Create virtual environment
- ✓ Install all dependencies
- ✓ Set up required directories

### 3.2 Upload LoRA Files (Optional)

If you have LoRA files locally:

```bash
# Place LoRA files in ./loras/ directory first
./runpod/sync_loras.sh
```

Or manually upload via SCP:
```bash
scp -i ~/.ssh/runpod_key -P YOUR_PORT your_lora.safetensors root@YOUR_HOST:/workspace/sdxl_image_generator/loras/
```

---

## Step 4: Running Generation

### 4.1 Connect to RunPod

```bash
./runpod/connect.sh
```

### 4.2 Navigate to Project

```bash
cd /workspace/sdxl_image_generator
source venv/bin/activate
```

### 4.3 Generate Images

Basic image generation:
```bash
python generate.py \
  --prompt "a beautiful landscape with mountains" \
  --device cuda \
  --width 1024 \
  --height 1024 \
  --steps 30
```

With LoRA:
```bash
python generate.py \
  --prompt "your prompt here" \
  --lora ./loras/your_lora.safetensors \
  --lora-scale 0.8 \
  --device cuda \
  --steps 30
```

### 4.4 Generate Videos

From existing image:
```bash
python generate_video.py \
  --image ./outputs/your_image.png \
  --num-frames 25 \
  --fps 6 \
  --device cuda
```

Complete workflow (image + video):
```bash
python workflow_img2vid.py \
  --prompt "portrait of a person" \
  --lora ./loras/your_lora.safetensors \
  --num-frames 25 \
  --fps 6 \
  --device cuda
```

### 4.5 Download Results

From your local machine:

```bash
# Download generated files
scp -i ~/.ssh/runpod_key -P YOUR_PORT -r \
  root@YOUR_HOST:/workspace/sdxl_image_generator/outputs/* \
  ./local_outputs/
```

---

## Step 5: Cost Management

### 5.1 Start Cost Tracking

Before running generations:
```bash
python runpod/cost_monitor.py start --gpu "RTX 4090" --pod-id YOUR_POD_ID
```

### 5.2 Estimate Costs

Estimate before running:
```bash
python runpod/cost_monitor.py estimate \
  --gpu "RTX 4090" \
  --images 10 \
  --videos 3 \
  --time-per-image 30 \
  --time-per-video 120
```

### 5.3 End Session

When done:
```bash
python runpod/cost_monitor.py end
```

### 5.4 View Summary

```bash
python runpod/cost_monitor.py summary
```

### 5.5 Stop Your Pod

**IMPORTANT**: Always stop your pod when not in use!

1. Go to RunPod console
2. Find your pod
3. Click "Stop" (or "Terminate" if done permanently)

---

## Performance Benchmarking

### Run Benchmark Tests

On RunPod:

```bash
cd /workspace/sdxl_image_generator
source venv/bin/activate

# Benchmark everything
python runpod/benchmark.py --test-all --device cuda

# Benchmark specific tests
python runpod/benchmark.py --test-image --device cuda
python runpod/benchmark.py --test-video --device cuda

# With LoRA
python runpod/benchmark.py --test-image --lora ./loras/your_lora.safetensors
```

### Typical Performance (RTX 4090)

| Task | Time | Cost (@ $0.69/hr) |
|------|------|-------------------|
| 1024x1024 image (30 steps) | ~15-30s | $0.003-0.006 |
| 25-frame video (~4s) | ~2-3min | $0.023-0.035 |
| Image + Video workflow | ~3-4min | $0.035-0.046 |

---

## Workflow Examples

### Example 1: Batch Image Generation

Generate 10 images with LoRA:

```bash
for i in {1..10}; do
  python generate.py \
    --prompt "your prompt $i" \
    --lora ./loras/your_lora.safetensors \
    --seed $i \
    --device cuda
done
```

### Example 2: Video Collection

Generate multiple videos from different images:

```bash
# First generate images
python generate.py --prompt "scene 1" --device cuda
python generate.py --prompt "scene 2" --device cuda
python generate.py --prompt "scene 3" --device cuda

# Then convert each to video
for img in outputs/generated_*.png; do
  python generate_video.py \
    --image "$img" \
    --num-frames 25 \
    --device cuda
done
```

### Example 3: Quality Test

Test different settings:

```bash
# Quick preview (20 steps)
python generate.py --prompt "test" --steps 20 --device cuda

# Balanced quality (30 steps)
python generate.py --prompt "test" --steps 30 --device cuda

# High quality (50 steps)
python generate.py --prompt "test" --steps 50 --device cuda
```

---

## Troubleshooting

### Connection Issues

**Can't connect via SSH:**
1. Check your SSH public key is added to RunPod
2. Verify pod is running (not stopped)
3. Check SSH host and port in `runpod_config.json`
4. Try connecting with verbose output:
   ```bash
   ssh -vvv -i ~/.ssh/runpod_key -p PORT root@HOST
   ```

### Out of Memory

**CUDA out of memory:**
1. Reduce image resolution: `--width 768 --height 768`
2. Reduce inference steps: `--steps 20`
3. For video, reduce frames: `--num-frames 14`
4. Use lower decode chunk size: `--decode-chunk-size 4`

### Slow Generation

**Generation is slower than expected:**
1. Verify GPU is being used: `nvidia-smi` (should show GPU activity)
2. Check if model is cached (first run downloads ~7GB)
3. Enable optimizations in code (already enabled)
4. Consider upgrading to faster GPU

### Model Download Issues

**Models not downloading:**
1. Check internet connection on pod
2. Verify HuggingFace is accessible
3. Try manual download:
   ```bash
   huggingface-cli download stabilityai/stable-diffusion-xl-base-1.0
   ```

### File Transfer Issues

**Can't download outputs:**
1. Check SSH key and permissions
2. Verify files exist: `ls /workspace/sdxl_image_generator/outputs/`
3. Try with `-v` flag for verbose output
4. Alternative: Use RunPod file browser in web console

---

## Cost Optimization Tips

1. **Use the right GPU**: RTX 3090/4090 is sufficient for most tasks
2. **Stop when idle**: Always stop your pod when not generating
3. **Batch operations**: Generate multiple items in one session
4. **Optimize parameters**: Lower steps/resolution for testing
5. **Use persistent volume**: Saves model download time
6. **Monitor costs**: Use the cost tracking tool regularly

---

## Advanced Configuration

### Custom Models

To use custom SDXL models:

1. Upload model to RunPod:
   ```bash
   scp -i ~/.ssh/runpod_key -P PORT your_model.safetensors root@HOST:/workspace/models/
   ```

2. Use with `--model` flag:
   ```bash
   python generate.py --model /workspace/models/your_model.safetensors --prompt "test"
   ```

### Video Settings

Adjust video quality and motion:

```bash
python generate_video.py \
  --image input.png \
  --num-frames 25 \              # More frames = longer video
  --fps 6 \                       # Higher fps = smoother (but shorter duration)
  --motion-bucket-id 180 \        # Higher = more motion (1-255)
  --noise-aug-strength 0.05 \     # Higher = more variation
  --device cuda
```

---

## Support

For issues:
1. Check RunPod status page
2. Review error messages carefully
3. Check GPU memory: `nvidia-smi`
4. Verify all files deployed: `ls -la /workspace/sdxl_image_generator/`

---

## Quick Reference

```bash
# Connect
./runpod/connect.sh

# Deploy
./runpod/deploy.sh

# Sync LoRAs
./runpod/sync_loras.sh

# Generate image
python generate.py --prompt "test" --device cuda

# Generate video
python generate_video.py --image input.png --device cuda

# Full workflow
python workflow_img2vid.py --prompt "test" --device cuda

# Benchmark
python runpod/benchmark.py --test-all --device cuda

# Cost tracking
python runpod/cost_monitor.py start --gpu "RTX 4090"
python runpod/cost_monitor.py end
python runpod/cost_monitor.py summary
```

---

**Remember**: Always stop your pod when done to avoid unnecessary charges!
