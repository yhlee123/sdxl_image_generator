# Prompt Templates & Best Practices

Quick reference for generating high-quality images for your platform.

---

## 🎨 Prompt Formula

```
[SUBJECT] + [POSE/ACTION] + [PHYSICAL DETAILS] + [SETTING] + [QUALITY TAGS]
```

---

## 📝 Subject Templates

### Base Character Descriptions

**Athletic/Fit Body:**
```
athletic body, toned abs, fit physique, sculpted muscles
```

**Curvy Body:**
```
curvy body, curvy hips, hourglass figure, voluptuous
```

**Petite/Slim:**
```
petite body, slim figure, slender physique
```

---

## 👤 Physical Attribute Options

### Ethnicity/Skin Tone
```
# Light Skin
fair skin, pale skin, porcelain skin

# Medium Skin
warm skin tone, olive skin, tan skin

# Dark Skin
dark skin, ebony skin, rich brown skin, deep skin tone
```

### Hair Styles
```
long flowing hair, ponytail, messy bun, hairpin bun, braided hair,
short bob, wavy hair, straight hair, curly hair, hair down
```

### Hair Colors
```
blonde hair, platinum blonde, brunette, black hair, red hair,
auburn hair, brown hair, dark hair, light hair
```

### Eye Colors
```
blue eyes, bright blue eyes, green eyes, brown eyes, hazel eyes,
dark eyes, striking eyes
```

### Facial Features
```
beautiful face, pretty face, supermodel face, (supermodel:1),
perfect face, detailed face, symmetrical face
```

### Breast Size
```
small breasts, medium breasts, large breasts, huge breasts,
perky breasts, natural breasts
```

---

## 💃 Pose/Action Templates

### Static Poses
```
# Standing
standing pose, standing upright, full body standing

# Sitting
sitting on sofa, sitting on chair, sitting pose, crossed legs

# Laying
laying down, laying on back, laying on side, reclining

# Leaning
leaning against wall, leaning forward, leaning back
```

### Dynamic/Action Poses (With LoRAs)
```
missionary position, getting fucked, vaginal sex,
legs up, legs spread, arched back
```

---

## 🎬 Setting/Background Templates

### Indoor
```
# Bedroom
in bedroom, on bed, luxury bedroom, modern bedroom

# Living Room
in living room, on sofa, on couch, modern interior

# Studio
studio lighting, photo studio, professional studio, white background

# Bathroom
in shower, in bathtub, bathroom setting
```

### Outdoor
```
outdoors, outdoor setting, in garden, at beach,
in nature, natural lighting, golden hour,
sunlight, sunny day, outdoors in the sun
```

### Lighting
```
# Natural Light
natural lighting, soft lighting, golden hour, sunset lighting,
diffused lighting

# Studio Light
studio lighting, professional lighting, dramatic lighting,
rim lighting, key light

# Special
warm lighting, cool lighting, backlit, side lighting
```

---

## ⭐ Quality Tags (Always Include!)

### Positive Quality Modifiers
```
photorealistic, realistic, high quality, best quality, masterpiece,
8k, ultra detailed, highly detailed, sharp focus, intricate details,
(perfect lighting:1.3), (incredible detail:1.3), professional photography
```

### Weight Examples
```
(masterpiece:1.2) = slightly emphasized
(best quality:1.5) = heavily emphasized
```

---

## 🚫 Negative Prompt (Standard)

```
ugly, poorly drawn face, poorly drawn hands, bad anatomy,
low quality, worst quality, blurry, out of focus,
cartoon, anime, 3d render, illustration, drawing,
painting, sketch, watermark, text, signature,
deformed, disfigured, malformed, mutated, extra limbs,
missing limbs, extra fingers, missing fingers,
bad proportions, unrealistic
```

### Additional Negative Tags (Optional)
```
# For More Realism
fake, artificial, plastic, smooth skin, glossy skin

# Remove Clothing
panties, bra, underwear, lingerie, clothes, clothed

# Remove Hair (if unwanted)
pubic hair, body hair, armpit hair

# Other
amateur, low resolution, pixelated, jpeg artifacts
```

---

## 🔥 Complete Example Prompts

### Example 1: Glamour Shot
```
Prompt:
close up photo of beautiful young woman, (supermodel:1.2),
athletic body, large breasts, fair skin, long blonde hair,
bright blue eyes, perfect face, laying on luxury sofa,
in modern living room, natural sunlight, golden hour lighting,
(photorealistic:1.3), (masterpiece:1.2), best quality,
8k, ultra detailed, professional photography

Negative:
ugly, poorly drawn face, hands, low quality, worst quality,
blurry, cartoon, anime, 3d render, panties, bra,
pubic hair, amateur
```

### Example 2: Active Pose (With LoRAs)
```
Prompt:
photo of athletic young woman getting missionary vaginal fucked,
(supermodel:1), curvy body, large breasts, warm brown skin,
dark hair, brown eyes, sweaty skin, legs up, laying on bed,
in bedroom, soft lighting, (perfect lighting:1.3),
(best quality:1.2), photorealistic, detailed penis, detailed vagina,
ultra detailed, intricate details

Negative:
ugly, poorly drawn face, hands, bad anatomy, low quality,
worst quality, blurry, cartoon, anime, 3d render,
pubic hair, amateur, panties, bra
```

### Example 3: Portrait Style
```
Prompt:
portrait of beautiful young woman, (supermodel:1.3),
petite body, medium breasts, olive skin, brunette wavy hair,
green eyes, pretty face, smiling, professional studio lighting,
white background, (photorealistic:1.4), (masterpiece:1.3),
best quality, 8k, highly detailed face, sharp focus

Negative:
ugly, poorly drawn face, low quality, worst quality, blurry,
cartoon, anime, 3d render, multiple people, group, text, watermark
```

### Example 4: Outdoor Scene
```
Prompt:
full body photo of gorgeous young woman, athletic body,
medium breasts, tan skin, long red hair, blue eyes,
standing outdoors in garden, sunny day, natural lighting,
(perfect lighting:1.2), golden hour, photorealistic,
(best quality:1.3), ultra detailed, professional photography

Negative:
ugly, poorly drawn face, hands, low quality, worst quality,
blurry, cartoon, anime, 3d render, clothes, bra, panties,
pubic hair, amateur, bad anatomy
```

---

## 🎯 Character Archetype Templates

### The Glamour Model
```
Prompt:
close up photo of stunning young woman, (supermodel:1.3),
voluptuous body, large breasts, fair porcelain skin,
platinum blonde long hair, striking blue eyes, perfect symmetrical face,
laying on luxury white sofa, high-end penthouse,
dramatic studio lighting, (photorealistic:1.4), (masterpiece:1.3),
best quality, 8k, ultra detailed, professional fashion photography

Negative:
ugly, poorly drawn face, hands, low quality, worst quality,
blurry, cartoon, anime, 3d render, pubic hair, amateur
```

### The Athletic Type
```
Prompt:
photo of athletic young woman, toned body, sculpted abs,
perky medium breasts, warm tan skin, ponytail brunette hair,
brown eyes, fit physique, stretching pose, in gym setting,
natural lighting, (photorealistic:1.3), best quality,
highly detailed, professional photography

Negative:
ugly, poorly drawn face, hands, low quality, worst quality,
blurry, cartoon, anime, 3d render, clothes, excessive muscles,
pubic hair
```

### The Girl Next Door
```
Prompt:
photo of cute young woman, natural beauty, slim petite body,
small perky breasts, fair skin with freckles, wavy auburn hair,
green eyes, sweet smile, sitting on bed, cozy bedroom,
soft natural lighting, (photorealistic:1.2), best quality,
detailed, warm tones

Negative:
ugly, poorly drawn face, hands, low quality, worst quality,
blurry, cartoon, anime, 3d render, heavy makeup, glamour
```

### The Exotic Beauty
```
Prompt:
photo of exotic young woman, hourglass curvy body,
large breasts, rich brown skin, long silky black hair,
dark almond eyes, sultry expression, reclining on chaise lounge,
luxury interior, warm golden lighting, (photorealistic:1.3),
(masterpiece:1.2), best quality, 8k, highly detailed

Negative:
ugly, poorly drawn face, hands, low quality, worst quality,
blurry, cartoon, anime, 3d render, pubic hair, amateur
```

---

## ⚙️ Generation Settings

### For High Quality Images
```bash
--steps 35-50           # More steps = better quality (diminishing returns after 50)
--guidance-scale 7.5    # Sweet spot for SDXL
--width 768             # Portrait
--height 1024
--dtype float32         # Better quality on Mac (use float16 on CUDA for speed)
--lora-scale 0.8        # Good balance, adjust 0.6-1.0 as needed
```

### For Fast Testing
```bash
--steps 20-25
--guidance-scale 7.0
--width 512
--height 768
--dtype float16
```

---

## 🧪 Testing Strategy

### Day 1: Test Basics
Generate 10 images testing:
1. Different body types (athletic, curvy, petite)
2. Different ethnicities/skin tones
3. Different hair colors/styles
4. Different lighting (studio, natural, dramatic)
5. Different poses (standing, sitting, laying)

### Day 2: Test Extremes
Generate 10 images testing:
1. Extreme close-ups vs full body
2. Very high steps (60-70) vs low (15-20)
3. Different guidance scales (5.0-12.0)
4. Different LoRA weights (0.5-1.5)
5. Complex prompts vs simple prompts

### Day 3: Test Best Settings
Based on Day 1-2 results:
- Generate 30 images with your optimal settings
- Vary only the character descriptions
- Create a "lookbook" of different character types

---

## 📊 Tracking What Works

Create a spreadsheet to track:

| Image # | Body Type | Skin Tone | Hair | Eyes | Pose | Setting | Steps | Guidance | LoRA Scale | Quality (1-10) | Notes |
|---------|-----------|-----------|------|------|------|---------|-------|----------|------------|----------------|-------|
| 001 | Athletic | Fair | Blonde | Blue | Standing | Studio | 35 | 7.5 | 0.8 | 9 | Perfect! |
| 002 | Curvy | Tan | Brunette | Brown | Sitting | Sofa | 35 | 7.5 | 0.8 | 7 | Hands off |

This helps you identify patterns in what works best!

---

## 🎨 Pro Tips

1. **Be Specific**: "Long flowing blonde hair" > "nice hair"
2. **Use Weights**: Emphasize important features with (term:1.2-1.5)
3. **Lighting Matters**: Good lighting descriptions = better results
4. **LoRA Balance**: Too high (>1.2) can cause artifacts
5. **Negative Prompts**: Don't skip these! They prevent common issues
6. **Seed Consistency**: Use same seed for variations on a character
7. **Batch Generate**: Generate 3-5 at once, pick the best
8. **Iterate**: Start simple, add details gradually

---

## 🚀 Batch Generation Script

Save time with batch generation:

```python
# batch_generate.py
import subprocess
import time

characters = [
    {
        "name": "blonde_athletic",
        "prompt": "athletic body, fair skin, long blonde hair, blue eyes, ...",
        "count": 5
    },
    {
        "name": "brunette_curvy",
        "prompt": "curvy body, tan skin, brunette hair, brown eyes, ...",
        "count": 5
    },
    # Add more...
]

for char in characters:
    for i in range(char["count"]):
        cmd = f"""
        python generate.py \
          --prompt "{char['prompt']}" \
          --negative-prompt "ugly, poorly drawn face, ..." \
          --steps 35 \
          --width 768 \
          --height 1024
        """
        subprocess.run(cmd, shell=True)
        time.sleep(5)  # Brief pause between generations
```

---

## 📝 Notes

- Save your best prompts in this file
- Update with new discoveries
- Share winning prompts with your developer
- Use these as defaults in your app's character creation

**Last Updated**: 2025-10-17
