# Product Specification: AI Character Generation Platform (MVP)

## Project Overview
Build a web application that allows users to generate photorealistic images and videos of AI-generated female characters using Stable Diffusion XL and custom LoRAs. Users can create custom characters, generate content, and access a gallery of their creations.

**Benchmark/Reference**: ourdream.ai (UI/UX inspiration)

---

## Target Users
- Adults (18+) interested in AI-generated character content
- Both free and paid tiers
- Desktop and mobile users

---

## MVP Feature Set

### ✅ **In Scope (Must Have)**
1. User authentication (signup, login, password reset)
2. Character creation form with customization options
3. Image generation (SDXL + LoRAs)
4. Video generation (Stable Video Diffusion)
5. Character profile pages with media gallery
6. User dashboard (My Characters)
7. Explore page (view all user's characters)
8. Token-based payment system
9. Subscription tiers (Free, Starter, Pro)
10. Stripe payment integration
11. Responsive design (desktop + mobile)

### ❌ **Out of Scope (Future Phases)**
- Chat functionality with characters (Phase 2)
- Public character sharing/community features (Phase 2)
- Social features (likes, comments, follows) (Phase 2)
- Advanced editing tools (Phase 3)
- API access for third parties (Phase 3)

---

## Technical Architecture

### **Frontend**
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + Shadcn/ui component library
- **State**: Zustand or React Query
- **Auth**: NextAuth.js

### **Backend**
- **Framework**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL + Auth)
- **Storage**: Cloudflare R2 (images/videos)
- **Payments**: Stripe (subscriptions + one-time purchases)
- **Queue**: Redis + Celery (optional for MVP, can use Replicate instead)

### **AI Generation**
- **Option A (Recommended)**: Replicate.com API
  - Pre-deployed SDXL + SVD models
  - Simple API integration
  - Pay-per-use ($0.002-0.01/image, $0.05/video)

- **Option B**: Custom RunPod integration
  - More control but complex
  - Requires DevOps

**Decision for MVP**: Use Replicate.com

### **Hosting/Deployment**
- **Frontend**: Vercel (free tier, auto-deploy from GitHub)
- **Backend**: Railway.app or Render.com
- **Database**: Supabase (free tier: 500MB, 2GB bandwidth)
- **Storage**: Cloudflare R2 (free tier: 10GB)

---

## Database Schema

### **users**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  subscription_tier VARCHAR(50) DEFAULT 'free',
  tokens_remaining INT DEFAULT 0,
  stripe_customer_id VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### **characters**
```sql
CREATE TABLE characters (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  name VARCHAR(255) NOT NULL,

  -- Physical appearance
  age_range VARCHAR(50),
  ethnicity VARCHAR(100),
  body_type VARCHAR(100),
  hair_style VARCHAR(100),
  hair_color VARCHAR(50),
  eye_color VARCHAR(50),
  skin_tone VARCHAR(50),

  -- Custom attributes
  custom_description TEXT,

  -- Metadata
  total_images INT DEFAULT 0,
  total_videos INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### **media**
```sql
CREATE TABLE media (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  character_id UUID REFERENCES characters(id) ON DELETE CASCADE,
  type VARCHAR(20) NOT NULL, -- 'image' or 'video'
  url TEXT NOT NULL, -- R2 storage URL
  thumbnail_url TEXT, -- For videos

  -- Generation parameters (stored as JSONB)
  generation_params JSONB,

  -- Metadata
  file_size_bytes BIGINT,
  width INT,
  height INT,
  duration_seconds FLOAT, -- For videos only

  created_at TIMESTAMP DEFAULT NOW()
);
```

### **subscriptions**
```sql
CREATE TABLE subscriptions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  stripe_subscription_id VARCHAR(255) UNIQUE,
  tier VARCHAR(50) NOT NULL, -- 'starter', 'pro'
  status VARCHAR(50) NOT NULL, -- 'active', 'cancelled', 'past_due'
  current_period_start TIMESTAMP,
  current_period_end TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

### **token_purchases**
```sql
CREATE TABLE token_purchases (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  stripe_payment_intent_id VARCHAR(255) UNIQUE,
  tokens_purchased INT NOT NULL,
  amount_paid_cents INT NOT NULL,
  status VARCHAR(50) NOT NULL, -- 'pending', 'completed', 'failed'
  created_at TIMESTAMP DEFAULT NOW()
);
```

---

## API Endpoints

### **Authentication**
```
POST   /api/auth/signup
POST   /api/auth/login
POST   /api/auth/logout
POST   /api/auth/reset-password
GET    /api/auth/me
```

### **Characters**
```
POST   /api/characters              # Create character
GET    /api/characters              # List user's characters
GET    /api/characters/:id          # Get character details
PUT    /api/characters/:id          # Update character
DELETE /api/characters/:id          # Delete character
```

### **Generation**
```
POST   /api/generate/image          # Generate character images
POST   /api/generate/video          # Generate character video from image
GET    /api/generate/status/:jobId  # Check generation status
```

### **Media**
```
GET    /api/media?character_id=:id  # Get character's media
GET    /api/media/:id               # Get single media item
DELETE /api/media/:id               # Delete media
```

### **Payments**
```
POST   /api/payments/create-subscription
POST   /api/payments/purchase-tokens
POST   /api/payments/webhook        # Stripe webhook
GET    /api/payments/billing-history
POST   /api/payments/cancel-subscription
```

### **User**
```
GET    /api/user/usage-stats        # Get user's token usage, generation count
GET    /api/user/subscription       # Get current subscription details
```

---

## User Flows

### **1. New User Signup & First Generation**
1. Land on homepage → See demo content
2. Click "Get Started" → Sign up form
3. After signup → Redirected to Character Creation
4. Fill out character form → Submit
5. System generates initial images (uses free credits)
6. View character profile with generated images
7. Option to generate video (requires tokens/subscription)

### **2. Paid User Workflow**
1. User runs out of free tokens
2. Prompted to upgrade or buy tokens
3. Click "Upgrade" → Pricing page
4. Select tier → Stripe checkout
5. After payment → Tokens/subscription activated
6. Return to generation

### **3. Generate Content Flow**
1. Go to character profile
2. Click "Generate More Images" or "Generate Video"
3. (Optional) Adjust settings (pose, clothing, etc.)
4. Confirm → Deduct tokens → Start generation
5. Show loading state with estimated time
6. On completion → Display new media in gallery

---

## Pricing Tiers

### **Free Tier**
- 3 image generations on signup
- Limited quality (fewer steps)
- Watermarked images (optional)
- No video generation
- Max 1 character

### **Starter ($9.99/month)**
- 50 image generations/month
- 5 video generations/month
- Full quality
- No watermarks
- Up to 5 characters
- Priority queue

### **Pro ($29.99/month)**
- 200 image generations/month
- 30 video generations/month
- Full quality
- No watermarks
- Unlimited characters
- Highest priority queue
- Advanced customization options

### **Token Packs (One-time purchases)**
- 50 tokens: $4.99
- 100 tokens: $8.99
- 250 tokens: $19.99

**Token Usage:**
- 1 image = 1 token
- 1 video (4 sec) = 5 tokens
- 1 video (6 sec) = 8 tokens

---

## UI/UX Pages & Components

### **Landing Page** (`/`)
**Layout:**
```
┌─────────────────────────────────────────────┐
│ [Logo]  Explore  Pricing  Login  Sign Up   │ ← Nav
├─────────────────────────────────────────────┤
│                                             │
│     Create Your Perfect AI Character        │ ← Hero
│           [Get Started Free]                │
│                                             │
├─────────────────────────────────────────────┤
│  [Character 1] [Character 2] [Character 3]  │ ← Demo Grid
│  [Character 4] [Character 5] [Character 6]  │
├─────────────────────────────────────────────┤
│     How It Works  |  Features  |  Pricing   │ ← Sections
└─────────────────────────────────────────────┘
```

### **Character Creation** (`/create`)
```
┌─────────────────────────────────────────────┐
│  Create New Character                       │
├─────────────────────────────────────────────┤
│  Character Name: [_____________]            │
│                                             │
│  Physical Appearance:                       │
│  ┌─ Age Range:     [20-25 ▼]              │
│  ├─ Ethnicity:     [Caucasian ▼]          │
│  ├─ Body Type:     [Athletic ▼]           │
│  ├─ Hair Style:    [Long ▼]               │
│  ├─ Hair Color:    [Blonde ▼]             │
│  ├─ Eye Color:     [Blue ▼]               │
│  └─ Skin Tone:     [Fair ▼]               │
│                                             │
│  Custom Description (optional):             │
│  [_________________________________]        │
│  [_________________________________]        │
│                                             │
│         [Cancel]  [Create Character]        │
└─────────────────────────────────────────────┘
```

### **Character Profile** (`/character/[id]`)
```
┌─────────────────────────────────────────────┐
│  ← Back to My Characters                    │
├─────────────────────────────────────────────┤
│  Character Name            [Edit] [Delete]  │
│  ──────────────────────────────────────────│
│  │ Appearance Info │                        │
│  │ Age: 20-25     │   [Generate Images]    │
│  │ Body: Athletic │   [Generate Video]     │
│  │ Hair: Blonde   │                        │
│  └────────────────┘                        │
├─────────────────────────────────────────────┤
│  Gallery (12 images, 3 videos)              │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐  │
│  │ Image │ │ Image │ │ Image │ │ Video │  │
│  └───────┘ └───────┘ └───────┘ └───────┘  │
│  ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐  │
│  │ Image │ │ Image │ │ Image │ │ Image │  │
│  └───────┘ └───────┘ └───────┘ └───────┘  │
└─────────────────────────────────────────────┘
```

### **My Characters** (`/dashboard`)
```
┌─────────────────────────────────────────────┐
│  My Characters      [+ Create New]          │
├─────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐        │
│  │ [Thumbnail]  │  │ [Thumbnail]  │        │
│  │ Character 1  │  │ Character 2  │        │
│  │ 12 images    │  │ 8 images     │        │
│  │ 2 videos     │  │ 1 video      │        │
│  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────┘
```

### **Pricing Page** (`/pricing`)
```
┌─────────────────────────────────────────────┐
│  Choose Your Plan                           │
├─────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────┐    │
│  │  FREE   │  │ STARTER │  │   PRO   │    │
│  │  $0/mo  │  │ $9.99   │  │ $29.99  │    │
│  │         │  │         │  │         │    │
│  │ Features│  │ Features│  │ Features│    │
│  │   ...   │  │   ...   │  │   ...   │    │
│  │         │  │         │  │         │    │
│  │ [Current│  │[Upgrade]│  │[Upgrade]│    │
│  └─────────┘  └─────────┘  └─────────┘    │
│                                             │
│  Or Buy Tokens:                             │
│  [50 - $4.99] [100 - $8.99] [250 - $19.99] │
└─────────────────────────────────────────────┘
```

---

## Design System

### **Colors** (Dark Theme - inspired by ourdream.ai)
```css
--background: #0a0a0f        /* Dark navy/black */
--surface: #1a1a24           /* Slightly lighter surface */
--primary: #8b5cf6           /* Purple */
--primary-hover: #7c3aed
--secondary: #ec4899         /* Pink accent */
--text-primary: #ffffff
--text-secondary: #9ca3af    /* Gray text */
--border: #2d2d3d            /* Subtle borders */
```

### **Typography**
- **Font**: Inter or similar sans-serif
- **Headings**: Bold, 2xl-4xl
- **Body**: Regular, base-lg
- **Buttons**: Semibold, sm-base

### **Components**
- **Buttons**: Rounded (md), with hover effects, gradient for primary CTA
- **Cards**: Dark surface, subtle border, hover lift effect
- **Forms**: Dark inputs with focus ring (purple)
- **Images**: Lazy loading, blur placeholder, aspect-ratio preserved
- **Loading**: Skeleton shimmer effect

---

## Generation Parameters

### **Image Generation** (SDXL + LoRAs)
```python
{
  "model": "stabilityai/stable-diffusion-xl-base-1.0",
  "loras": [
    "./loras/MissionaryVaginal-v1-SDXL.safetensors",
    "./loras/topless_v1a_fro0_95.safetensors",
    "./loras/f865513d-a5e9-4b5e-8e4e-82db39442444.safetensors"
  ],
  "lora_scale": 0.8,
  "width": 768,
  "height": 1024,
  "steps": 35,  # Free: 20, Paid: 35-50
  "guidance_scale": 7.5,
  "negative_prompt": "ugly, poorly drawn face, hands, low quality, worst quality, blurry, cartoon, anime, 3d render"
}
```

### **Video Generation** (SVD)
```python
{
  "model": "stabilityai/stable-video-diffusion-img2vid-xt",
  "num_frames": 25,  # ~4 seconds at 6fps
  "fps": 6,
  "motion_bucket_id": 127,  # Moderate motion
  "noise_aug_strength": 0.02,
  "device": "cuda",
  "dtype": "float16"
}
```

---

## Success Metrics (Post-Launch)

### **Week 1 Goals**
- 100 signups
- 50 active users
- 500+ image generations
- 5 paying customers

### **Month 1 Goals**
- 500 signups
- 50 paying customers
- $500 MRR (Monthly Recurring Revenue)

### **Key Metrics to Track**
- Conversion rate (free → paid)
- Average tokens used per user
- Generation success rate
- Page load times
- User retention (Day 1, Day 7, Day 30)

---

## Developer Handoff Checklist

### **What the Developer Should Deliver:**
- [ ] Complete codebase in GitHub repository
- [ ] Frontend deployed to Vercel
- [ ] Backend deployed to Railway/Render
- [ ] Database set up on Supabase
- [ ] Stripe integration configured (test mode)
- [ ] Environment variables documented
- [ ] README with setup instructions
- [ ] Loom video walkthrough of codebase
- [ ] Basic admin panel to view users/stats

### **Documentation Needed:**
- [ ] API endpoints documentation
- [ ] Database schema diagram
- [ ] Environment variables list
- [ ] Deployment guide
- [ ] How to add/modify generation parameters
- [ ] How to test payments (Stripe test mode)

---

## Timeline Estimate

### **Week 1-2: Core Development**
- Authentication system
- Database setup
- Basic UI (landing, signup, login)
- Character creation form

### **Week 3: Generation Integration**
- Replicate API integration
- Image generation endpoint
- Video generation endpoint
- Storage (R2) setup

### **Week 4: Polish & Payments**
- Stripe integration
- Pricing page
- Token system
- Gallery views
- Mobile responsive fixes

### **Week 5: Testing & Launch**
- Bug fixes
- Performance optimization
- Content moderation setup
- Beta testing
- Launch

---

## Questions for Developer Interview

1. Have you built subscription/payment systems with Stripe before?
2. Experience with Next.js 14 (App Router)?
3. Familiar with Supabase or similar BaaS?
4. Can you integrate with Replicate or similar AI APIs?
5. Show examples of dark-themed, modern UI you've built
6. Availability for 2-4 weeks of work?
7. Post-launch support options?

---

## Budget Allocation

| Item | Cost |
|------|------|
| Developer (2-3 weeks) | $1,500-2,000 |
| Vercel (Pro, if needed) | $20/mo |
| Supabase (Free tier OK for MVP) | $0 |
| Cloudflare R2 | ~$10-20/mo |
| Replicate (generation costs) | ~$50-100/mo |
| Stripe (transaction fees) | 2.9% + $0.30 per transaction |
| Domain | $12/year |
| **Total Initial** | **~$1,600-2,200** |
| **Monthly Recurring** | **~$80-140/mo** |

---

## Next Steps

1. ✅ Review this spec
2. → Post job on Upwork/Fiverr
3. → Interview 3-5 developers
4. → Select developer, sign contract
5. → Daily check-ins during development
6. → Testing & feedback
7. → Launch!
