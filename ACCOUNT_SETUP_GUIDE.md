# Account Setup Guide

Complete this checklist before your developer starts working. Most services have free tiers that are perfect for MVP testing.

---

## ☐ 1. Domain Name Registration

**Recommended Services:**
- **Namecheap** (namecheap.com) - Good prices, easy management
- **GoDaddy** (godaddy.com) - Popular, slightly pricier
- **Porkbun** (porkbun.com) - Cheapest, great for .com/.ai domains

**Domain Suggestions:**
- `aicharacter.app` or `.ai`
- `dreamcharacter.ai`
- `[yourprojectname].ai` or `.app` or `.co`

**Cost**: $10-30/year

**Steps:**
1. Go to Namecheap.com
2. Search for your desired domain
3. Purchase (1 year to start)
4. You'll configure DNS later when deploying

---

## ☐ 2. Vercel Account (Frontend Hosting)

**URL**: https://vercel.com

**Plan**: Free (Hobby) - Upgrade to Pro ($20/mo) only if needed

**Steps:**
1. Sign up with GitHub account (recommended)
2. No credit card required for free tier
3. Your developer will connect the Next.js project later

**What it includes:**
- Unlimited deployments
- Auto-deploy from GitHub
- Free SSL certificate
- Global CDN
- 100GB bandwidth/month

---

## ☐ 3. Supabase Account (Database + Auth)

**URL**: https://supabase.com

**Plan**: Free tier (perfect for MVP)

**Steps:**
1. Sign up with GitHub
2. Create a new project:
   - Project name: `[yourprojectname]-prod`
   - Database password: Generate a strong one, save it!
   - Region: Choose closest to your users (e.g., US East, US West)
3. Wait 2-3 minutes for project to provision
4. Save these credentials (found in Project Settings → API):
   - `SUPABASE_URL`
   - `SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY` (secret!)
   - Database connection string

**What it includes (Free tier):**
- 500MB database
- 1GB file storage
- 2GB bandwidth
- Unlimited API requests
- Built-in authentication

---

## ☐ 4. Cloudflare R2 (Image/Video Storage)

**URL**: https://dash.cloudflare.com/sign-up

**Plan**: Free tier (10GB storage, no egress fees!)

**Steps:**
1. Sign up for Cloudflare account
2. Go to R2 in sidebar
3. Click "Purchase R2 Plan"
4. Create a bucket:
   - Name: `[yourprojectname]-media`
   - Region: Automatic
5. Create API token:
   - Go to "Manage R2 API Tokens"
   - Click "Create API Token"
   - Permissions: Read & Write
   - Save the Access Key ID and Secret Access Key

**Save these:**
- `R2_ACCOUNT_ID`
- `R2_ACCESS_KEY_ID`
- `R2_SECRET_ACCESS_KEY`
- `R2_BUCKET_NAME`
- `R2_PUBLIC_URL` (you'll set up a custom domain later)

**What it includes (Free tier):**
- 10GB storage
- 10 million Class A operations/month
- 10 million Class B operations/month
- No egress fees (huge savings vs S3!)

---

## ☐ 5. Stripe Account (Payments)

**URL**: https://dashboard.stripe.com/register

**Plan**: Free (only pay transaction fees when you make money)

**Steps:**
1. Sign up with email
2. Complete business verification (required before going live)
3. Enable test mode (toggle in top right)
4. Create products in Test Mode:
   - Go to Products → Add Product
   - **Starter Plan**: $9.99/month recurring
   - **Pro Plan**: $29.99/month recurring
   - **50 Tokens**: $4.99 one-time
   - **100 Tokens**: $8.99 one-time
   - **250 Tokens**: $19.99 one-time

5. Get API keys:
   - Go to Developers → API Keys
   - Copy "Publishable key" and "Secret key" (test mode)

**Save these:**
- `STRIPE_PUBLISHABLE_KEY_TEST`
- `STRIPE_SECRET_KEY_TEST`
- `STRIPE_WEBHOOK_SECRET` (create after deployment)

**Fees:**
- 2.9% + $0.30 per transaction
- No monthly fees

---

## ☐ 6. Replicate Account (AI Generation)

**URL**: https://replicate.com/signin

**Plan**: Pay-per-use (no monthly fees)

**Steps:**
1. Sign up with GitHub
2. Add a payment method (credit card)
3. Get API token:
   - Go to Account → API Tokens
   - Create new token
   - Copy the token

**Save this:**
- `REPLICATE_API_TOKEN`

**Costs (approximate):**
- SDXL image generation: $0.002-0.005 per image
- SVD video generation: $0.03-0.05 per video (25 frames)
- Expect ~$50-100/month for initial testing

**Models you'll use:**
- `stability-ai/sdxl`
- `stability-ai/stable-video-diffusion-img2vid-xt`

---

## ☐ 7. Railway or Render (Backend Hosting)

### **Option A: Railway.app** (Recommended)

**URL**: https://railway.app

**Plan**: Free $5 credit/month, then pay-as-you-go

**Steps:**
1. Sign up with GitHub
2. No setup needed yet - developer will deploy later
3. Add credit card to get beyond free tier

**Cost**: ~$5-15/month for small FastAPI app

### **Option B: Render.com**

**URL**: https://render.com

**Plan**: Free tier available (spins down after inactivity)

**Steps:**
1. Sign up with GitHub
2. Free tier: Good for testing, but has cold starts
3. Paid tier ($7/mo): Always-on

---

## ☐ 8. GitHub Repository (Optional but Recommended)

**URL**: https://github.com

**Plan**: Free

**Steps:**
1. Create account (if you don't have one)
2. Create a new private repository:
   - Name: `[yourprojectname]-web`
   - Private
   - Don't initialize with README (developer will do this)
3. Add your developer as a collaborator

---

## ☐ 9. Email Service (For Password Reset, etc.)

**Recommended: Resend** (easiest)

**URL**: https://resend.com

**Plan**: Free tier (100 emails/day)

**Steps:**
1. Sign up
2. Verify your domain later (after you have it)
3. Get API key

**Alternative**: Supabase has built-in email for auth (uses their domain)

---

## Summary: Credentials Checklist

Create a secure note (use 1Password, LastPass, or encrypted file) with these:

```env
# Domain
DOMAIN=yourdomain.com

# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJxxx...
SUPABASE_SERVICE_ROLE_KEY=eyJxxx... (SECRET!)

# Cloudflare R2
R2_ACCOUNT_ID=xxxxx
R2_ACCESS_KEY_ID=xxxxx
R2_SECRET_ACCESS_KEY=xxxxx (SECRET!)
R2_BUCKET_NAME=yourproject-media

# Stripe (Test Mode)
STRIPE_PUBLISHABLE_KEY_TEST=pk_test_xxxxx
STRIPE_SECRET_KEY_TEST=sk_test_xxxxx (SECRET!)

# Replicate
REPLICATE_API_TOKEN=r8_xxxxx (SECRET!)

# App Secrets (developer will generate)
NEXTAUTH_SECRET=xxxxx (SECRET!)
JWT_SECRET=xxxxx (SECRET!)
```

---

## Total Monthly Cost Estimate (MVP)

| Service | Free Tier | Paid (if needed) |
|---------|-----------|------------------|
| Domain | - | $10-30/year |
| Vercel | ✅ Free | $20/mo (Pro) |
| Supabase | ✅ Free | $25/mo (Pro) |
| Cloudflare R2 | ✅ Free (10GB) | $0.015/GB after |
| Stripe | ✅ Free | 2.9% per transaction |
| Replicate | - | ~$50-100/mo |
| Railway/Render | ✅ $5 credit | $5-15/mo |
| **TOTAL** | **~$50-100/mo** | **~$100-180/mo** |

**Note**: You can start with all free tiers except Replicate and scale as you grow!

---

## Next Steps

1. ✅ Complete all account signups (1-2 hours)
2. ✅ Save all credentials securely
3. ✅ Share credentials with developer (use secure method like 1Password share or encrypted file)
4. ✅ Post job on Upwork/Fiverr
5. ✅ Interview candidates
6. ✅ Start development!

---

## Security Best Practices

⚠️ **NEVER commit credentials to Git**
⚠️ **Use different passwords for each service**
⚠️ **Enable 2FA on all accounts**
⚠️ **Keep test mode credentials separate from production**
⚠️ **Only share credentials via secure channels (not email)**

---

## Questions?

If you run into issues setting up any service, most have excellent documentation and support chat. You can also ask me for help!
