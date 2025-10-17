# Job Posting: Full-Stack Developer for AI Character Generation Platform

## Project Title
**Build MVP Web App for AI Image/Video Generation Platform (Next.js + FastAPI)**

---

## Budget
**$1,800 USD** (Fixed Price)

---

## Project Duration
**2-3 weeks** (with possibility of ongoing maintenance work)

---

## Project Description

I'm looking for an experienced full-stack developer to build the MVP of an AI-powered character generation platform. The app allows users to create custom AI characters and generate photorealistic images and videos.

**This project is PERFECT for you if you have:**
✅ Strong Next.js 14+ (App Router) experience
✅ Python/FastAPI backend skills
✅ Experience with Stripe payments
✅ Modern UI/UX design sensibility (dark themes, shadcn/ui)
✅ API integration experience (we'll use Replicate for AI generation)

---

## What You'll Build

### **Frontend (Next.js 14 + TypeScript + Tailwind)**
- Landing page with hero section and demo content grid
- User authentication (signup, login, password reset)
- Character creation form with dropdowns and text inputs
- Character profile page with image/video gallery
- User dashboard showing all characters
- Pricing page with Stripe checkout
- Account/billing page
- Fully responsive (desktop + mobile)

### **Backend (FastAPI + Python)**
- REST API endpoints for all CRUD operations
- Supabase integration (PostgreSQL + Auth)
- Replicate API integration for image/video generation
- Stripe webhook handling for subscriptions & payments
- Token/credit system logic
- File upload to Cloudflare R2

### **Key Features**
1. **User Authentication**: Email/password signup, login, JWT tokens (using Supabase Auth or NextAuth)
2. **Character Management**: Create, read, update, delete characters
3. **AI Generation Integration**:
   - Call Replicate API for SDXL image generation
   - Call Replicate API for video generation (SVD)
   - Handle job queuing and status checks
4. **Payment System**:
   - Stripe subscriptions (3 tiers: Free, Starter $9.99, Pro $29.99)
   - One-time token purchases
   - Webhook for payment confirmation
5. **Token System**: Track user tokens, deduct on generation, refill on subscription renewal
6. **Media Gallery**: Display generated images/videos, lazy loading

---

## Tech Stack (Non-Negotiable)

### **Frontend**
- Next.js 14+ (App Router, TypeScript)
- Tailwind CSS + Shadcn/ui
- NextAuth.js or Supabase Auth

### **Backend**
- FastAPI (Python 3.9+)
- PostgreSQL via Supabase (free tier)
- Cloudflare R2 for storage (will provide API keys)

### **Third-Party Services**
- **Replicate.com**: AI generation API (I'll provide API key)
- **Stripe**: Payments (I'll provide test/live keys)
- **Supabase**: Database + Auth (I'll set up account)

### **Deployment**
- Frontend: Vercel
- Backend: Railway.app or Render.com

---

## Detailed Requirements

### **Database Schema**
You'll implement these tables in Supabase:
- `users`: User accounts, subscription tier, token balance
- `characters`: Character definitions (name, appearance attributes)
- `media`: Generated images/videos with URLs
- `subscriptions`: Stripe subscription tracking
- `token_purchases`: One-time token purchase history

(Full schema provided in attached spec document)

### **API Endpoints Required**
```
Authentication:
POST /api/auth/signup
POST /api/auth/login
GET /api/auth/me

Characters:
POST /api/characters
GET /api/characters
GET /api/characters/:id
PUT /api/characters/:id
DELETE /api/characters/:id

Generation:
POST /api/generate/image
POST /api/generate/video
GET /api/generate/status/:jobId

Media:
GET /api/media?character_id=:id
DELETE /api/media/:id

Payments:
POST /api/payments/create-subscription
POST /api/payments/purchase-tokens
POST /api/payments/webhook (Stripe)
POST /api/payments/cancel-subscription

User:
GET /api/user/usage-stats
GET /api/user/subscription
```

### **UI/UX Requirements**
- **Dark theme** (navy/black background, purple/pink accents)
- Clean, modern design similar to ourdream.ai
- Smooth animations (hover effects, page transitions)
- Responsive mobile design
- Loading states with skeleton shimmer
- Toast notifications for user feedback
- Image lazy loading with blur placeholders

---

## What I'll Provide

✅ Complete product specification document
✅ API keys for Replicate, Stripe (test mode), Cloudflare R2
✅ Supabase project set up
✅ Logo and brand colors
✅ Sample LoRA files and generation scripts (for reference)
✅ Daily availability for questions/clarifications

---

## Deliverables

### **Code & Deployment**
1. Complete source code in GitHub repository (private)
2. Frontend deployed to Vercel (connected to GitHub)
3. Backend deployed to Railway/Render
4. Database schema implemented in Supabase
5. Environment variables documented in `.env.example`

### **Documentation**
1. README with setup instructions
2. API endpoint documentation
3. How to run locally
4. How to deploy
5. **Loom video walkthrough** (15-20 min) explaining:
   - Project structure
   - Key components and files
   - How to modify generation parameters
   - How to add new features
   - How to test Stripe payments

### **Code Quality**
- Clean, well-commented code
- TypeScript types properly defined
- Error handling on all API calls
- Input validation (frontend + backend)
- Mobile-responsive (tested on iOS/Android)

---

## Milestones & Payment

### **Milestone 1** ($600 - Week 1)
- Project scaffolding (Next.js + FastAPI + Supabase)
- Authentication working
- Basic UI (landing, signup, login, dashboard)
- Database schema implemented

### **Milestone 2** ($600 - Week 2)
- Character CRUD complete
- Generation integration (Replicate API)
- Media gallery working
- R2 storage integration

### **Milestone 3** ($600 - Week 3)
- Stripe integration complete
- Token system working
- All pages finalized and responsive
- Deployed to production
- Documentation + Loom video

---

## Required Skills

**Must-Have:**
- ✅ Next.js 14 (App Router) - **at least 1 year experience**
- ✅ TypeScript - **proficient**
- ✅ FastAPI or similar Python web framework
- ✅ PostgreSQL and ORMs (Prisma/SQLAlchemy)
- ✅ Stripe API integration
- ✅ REST API design
- ✅ Responsive design (Tailwind CSS)
- ✅ Git/GitHub workflow
- ✅ English communication (for daily updates)

**Nice-to-Have:**
- Supabase experience
- Replicate or similar AI API experience
- Shadcn/ui component library
- Cloudflare R2 or S3 storage
- Adult content platform experience (bonus!)

---

## Application Requirements

**To apply, please include:**

1. **Relevant Portfolio Links** (2-3 projects)
   - Especially Next.js projects with dark themes
   - Any projects with Stripe integration

2. **Answer these questions:**
   - Have you built a payment/subscription system with Stripe before? (Yes/No + brief description)
   - Have you used Next.js 14 App Router? (Yes/No)
   - Have you integrated with third-party AI/ML APIs? (Yes/No + which ones)
   - What's your experience with Supabase or similar BaaS platforms?
   - Can you start immediately and commit to 2-3 weeks full-time?

3. **Availability:**
   - How many hours per day can you dedicate?
   - What timezone are you in?
   - Can you do a daily 15-min check-in call (via Zoom/Google Meet)?

4. **Pricing:**
   - Confirm the $1,800 fixed price works for you
   - Any additional costs for post-launch support?

---

## Interview Process

1. **Application Review** (1 day)
2. **Short Video Call** (30 min) - discuss project, review your portfolio
3. **Small Paid Test Task** (optional, $50, 2-3 hours)
   - Build a simple Next.js page with Stripe checkout
4. **Project Start** (sign contract, set up repos)

---

## Red Flags (Will NOT Hire If...)

❌ Generic "I can do this" messages without portfolio
❌ Copy-pasted proposals
❌ Unwilling to provide specific examples of past work
❌ Cannot commit to timeline
❌ Asking to change tech stack significantly
❌ Cannot do video calls for check-ins

---

## Additional Notes

- This is adult content (18+), but nothing illegal or unethical
- Must be comfortable working on this type of platform
- Potential for ongoing work (Phase 2: chat features, community)
- Great for portfolio if you can showcase it (can provide anonymized version)

---

## How to Stand Out

🌟 **Show me you've read this carefully** by starting your proposal with "AI Character Gen - [Your Name]"

🌟 **Include a Loom video** (2-3 min) walking through one of your relevant projects

🌟 **Propose improvements** - if you see ways to make the architecture better, let me know!

---

## Questions?

Feel free to ask any questions before applying. I'm very responsive and want to find the right developer for this project.

Looking forward to working with you!
