# SDXL Image Generator with LoRA Support

A general-purpose tool for generating images using Stable Diffusion XL (SDXL) with support for LoRA (Low-Rank Adaptation) models from Civitai and other sources.

## Features

- Generate high-quality images using SDXL base model
- Support for multiple LoRA models
- Configurable generation parameters
- Built-in presets for different use cases
- Metadata embedding in generated images
- Easy-to-use command-line interface
- Configuration file support for managing LoRAs

## Project Structure

```
sdxl_image_generator/
├── generate.py              # Main generation script
├── generate_with_config.py  # Config-based generation script
├── requirements.txt         # Python dependencies
├── configs/                 # Configuration files
│   └── example_config.json  # Example configuration
├── loras/                   # Store your LoRA files here
├── models/                  # Store model files here (optional)
└── outputs/                 # Generated images saved here
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
