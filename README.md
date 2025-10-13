# SDXL Image & Video Generator with LoRA Support

A general-purpose tool for generating images and videos using Stable Diffusion XL (SDXL) and Stable Video Diffusion (SVD), with support for LoRA (Low-Rank Adaptation) models from Civitai and other sources.

## Features

### Image Generation
- Generate high-quality images using SDXL base model
- Support for multiple LoRA models
- Configurable generation parameters
- Built-in presets for different use cases
- Metadata embedding in generated images

### Video Generation
- Generate videos from images using Stable Video Diffusion
- Complete image-to-video workflow
- Adjustable motion and frame count
- Support for 3-5 second clips (customizable)

### Cloud GPU Support
- **RunPod integration** for cloud GPU access
- Deployment scripts for easy setup
- Performance benchmarking tools
- Cost tracking and management utilities

### General
- Easy-to-use command-line interface
- Configuration file support for managing LoRAs
- Local and cloud deployment options

## Project Structure

```
sdxl_image_generator/
├── generate.py              # Main image generation script
├── generate_with_config.py  # Config-based generation script
├── generate_video.py        # Video generation script
├── workflow_img2vid.py      # Complete image-to-video workflow
├── requirements.txt         # Python dependencies
├── configs/                 # Configuration files
│   └── example_config.json  # Example configuration
├── loras/                   # Store your LoRA files here
├── models/                  # Store model files here (optional)
├── outputs/                 # Generated images and videos
└── runpod/                  # RunPod cloud GPU integration
    ├── README.md            # Complete RunPod setup guide
    ├── runpod_config.json   # RunPod configuration
    ├── connect.sh           # SSH connection script
    ├── deploy.sh            # Deployment script
    ├── sync_loras.sh        # LoRA sync script
    ├── benchmark.py         # Performance benchmarking
    └── cost_monitor.py      # Cost tracking utility
```

## Installation

The environment is already set up! The virtual environment is located in `venv/`.

To activate it:
```bash
source venv/bin/activate
```

To install dependencies manually (already done):
```bash
pip install -r requirements.txt
```

## Usage

### Method 1: Direct Command Line

Generate images with full control over all parameters:

```bash
# Basic usage
python generate.py --prompt "a beautiful landscape with mountains"

# With LoRA
python generate.py \
  --prompt "a beautiful landscape with mountains" \
  --lora ./loras/your_lora.safetensors \
  --lora-scale 0.8

# Multiple LoRAs
python generate.py \
  --prompt "portrait of a person" \
  --lora ./loras/lora1.safetensors \
  --lora ./loras/lora2.safetensors \
  --lora-scale 1.0

# Full control
python generate.py \
  --prompt "your prompt here" \
  --negative-prompt "low quality, blurry" \
  --width 1024 \
  --height 1024 \
  --steps 50 \
  --guidance-scale 8.0 \
  --num-images 4 \
  --seed 42 \
  --lora ./loras/your_lora.safetensors \
  --lora-scale 0.9
```

### Method 2: Using Configuration File

1. First, edit `configs/example_config.json` to add your LoRAs:

```json
{
  "loras": {
    "my_style_lora": {
      "path": "./loras/my_style.safetensors",
      "weight": 1.0,
      "enabled": true,
      "description": "My custom style LoRA"
    }
  }
}
```

2. Generate images using the config:

```bash
# Use enabled LoRAs from config
python generate_with_config.py \
  --config ./configs/example_config.json \
  --prompt "your prompt here"

# Use a specific preset
python generate_with_config.py \
  --config ./configs/example_config.json \
  --preset quality \
  --prompt "your prompt here"

# Enable specific LoRA by name
python generate_with_config.py \
  --config ./configs/example_config.json \
  --enable-lora my_style_lora \
  --prompt "your prompt here"
```

## Command Line Arguments

### generate.py

| Argument | Description | Default |
|----------|-------------|---------|
| `--model` | Model ID or path | stabilityai/stable-diffusion-xl-base-1.0 |
| `--device` | Device (mps/cuda/cpu) | mps |
| `--prompt` | Text prompt (required) | - |
| `--negative-prompt` | Negative prompt | "" |
| `--width` | Image width | 1024 |
| `--height` | Image height | 1024 |
| `--steps` | Number of inference steps | 30 |
| `--guidance-scale` | Guidance scale | 7.5 |
| `--num-images` | Number of images | 1 |
| `--seed` | Random seed | None (random) |
| `--lora` | LoRA file path (can use multiple) | [] |
| `--lora-scale` | LoRA weight/scale | 1.0 |
| `--output-dir` | Output directory | ./outputs |

### generate_with_config.py

| Argument | Description | Default |
|----------|-------------|---------|
| `--config` | Configuration file path | ./configs/example_config.json |
| `--preset` | Use preset (quick/quality/portrait/landscape) | None |
| `--prompt` | Text prompt (required) | - |
| `--enable-lora` | Enable specific LoRA by name | [] |
| `--num-images` | Number of images | 1 |
| `--seed` | Random seed | None |

## Video Generation

### Basic Video Generation

Generate a video from an existing image:

```bash
python generate_video.py \
  --image ./outputs/your_image.png \
  --num-frames 25 \
  --fps 6 \
  --device cuda
```

### Complete Image-to-Video Workflow

Generate an image with SDXL + LoRA, then create a video:

```bash
python workflow_img2vid.py \
  --prompt "portrait of a person, professional photography" \
  --lora ./loras/your_lora.safetensors \
  --num-frames 25 \
  --fps 6 \
  --device cuda
```

### Video Parameters

- `--num-frames`: Number of frames (25 = ~4 seconds at 6fps)
- `--fps`: Frames per second (6 recommended for SVD)
- `--motion`: Motion amount (1-255, higher = more motion, default: 127)
- `--device`: cuda for GPU, mps for Mac Metal, cpu for CPU

## Cloud GPU with RunPod

For faster generation with powerful GPUs, use RunPod cloud GPUs:

### Quick Start

1. **Setup RunPod Pod** (see `runpod/README.md` for details)
   - Choose RTX 3090/4090 or better (24GB+ VRAM)
   - Enable SSH access

2. **Configure Connection**
   ```bash
   # Edit runpod/runpod_config.json with your pod details
   # Your SSH key is already generated at ~/.ssh/runpod_key
   ```

3. **Deploy to RunPod**
   ```bash
   ./runpod/deploy.sh
   ```

4. **Connect and Generate**
   ```bash
   ./runpod/connect.sh
   # Now on RunPod:
   cd /workspace/sdxl_image_generator
   source venv/bin/activate
   python generate.py --prompt "test" --device cuda
   ```

### Cost Management

Track and estimate RunPod costs:

```bash
# Start tracking
python runpod/cost_monitor.py start --gpu "RTX 4090"

# Estimate before running
python runpod/cost_monitor.py estimate --gpu "RTX 4090" --images 10 --videos 3

# End session
python runpod/cost_monitor.py end

# View summary
python runpod/cost_monitor.py summary
```

### Performance Benchmarking

Benchmark your RunPod instance:

```bash
# On RunPod
python runpod/benchmark.py --test-all --device cuda
```

**For complete RunPod setup and usage, see [`runpod/README.md`](runpod/README.md)**

## Getting LoRAs from Civitai

1. Visit [Civitai.com](https://civitai.com)
2. Search for SDXL LoRAs (make sure they're compatible with SDXL, not SD1.5)
3. Download the `.safetensors` file
4. Place it in the `./loras/` directory
5. Add it to your config or use with `--lora` flag

## Configuration File

The configuration file (`configs/example_config.json`) allows you to:

- Set default model and device settings
- Manage multiple LoRAs with descriptions
- Define generation presets (quick, quality, portrait, landscape)
- Set default generation parameters

Example structure:

```json
{
  "model": {
    "model_id": "stabilityai/stable-diffusion-xl-base-1.0",
    "device": "mps",
    "dtype": "float16"
  },
  "loras": {
    "lora_name": {
      "path": "./loras/file.safetensors",
      "weight": 1.0,
      "enabled": false,
      "description": "Description"
    }
  },
  "generation_defaults": {
    "width": 1024,
    "height": 1024,
    "num_inference_steps": 30,
    "guidance_scale": 7.5,
    "negative_prompt": "low quality, blurry"
  },
  "presets": {
    "quality": {
      "num_inference_steps": 50,
      "guidance_scale": 8.0
    }
  }
}
```

## Tips for Best Results

1. **Prompt Quality**: Be descriptive and specific in your prompts
2. **LoRA Scale**: Start with 0.7-1.0, adjust based on results
   - Lower values (0.5-0.7): Subtle effect
   - Higher values (1.0-1.5): Strong effect
3. **Steps**: More steps = better quality but slower
   - Quick: 20-25 steps
   - Balanced: 30-35 steps
   - Quality: 40-60 steps
4. **Guidance Scale**: Higher = more prompt adherence
   - Creative: 5.0-7.0
   - Balanced: 7.0-9.0
   - Strict: 9.0-12.0
5. **Seeds**: Use the same seed for consistent results

## System Requirements

- **Mac (M1/M2/M3)**: Uses MPS (Metal Performance Shaders)
- **NVIDIA GPU**: Uses CUDA (change `--device cuda`)
- **CPU**: Slower but works (change `--device cpu`)

### Minimum Requirements
- 8GB RAM (16GB recommended)
- 10GB free disk space for models
- Python 3.8+

## Troubleshooting

### Out of Memory Errors
- Reduce image size (e.g., 512x512 or 768x768)
- Use fewer inference steps
- Close other applications
- Use float32 instead of float16: `--dtype float32`

### Model Download Issues
- The first run will download the SDXL model (~7GB)
- Ensure stable internet connection
- Models are cached in `~/.cache/huggingface/`

### LoRA Not Loading
- Verify the file is in `.safetensors` format
- Check the path is correct
- Ensure the LoRA is compatible with SDXL (not SD1.5)

## Examples

### Generate a portrait
```bash
python generate.py \
  --prompt "portrait of a person, professional photography, studio lighting" \
  --negative-prompt "low quality, blurry, distorted" \
  --width 768 \
  --height 1024 \
  --steps 35 \
  --guidance-scale 8.0
```

### Generate with LoRA
```bash
python generate.py \
  --prompt "artistic painting of a landscape" \
  --lora ./loras/artistic_style.safetensors \
  --lora-scale 0.8 \
  --steps 40
```

### Batch generation with seed
```bash
python generate.py \
  --prompt "futuristic cityscape at night" \
  --num-images 5 \
  --seed 12345 \
  --steps 30
```

## License

This tool is for general-purpose use. Please respect the licenses of the models and LoRAs you use.

## Credits

- Stable Diffusion XL by Stability AI
- Diffusers library by HuggingFace
- LoRA models from Civitai community

## Support

For issues or questions, check:
- [Diffusers Documentation](https://huggingface.co/docs/diffusers)
- [Civitai](https://civitai.com) for LoRA information
