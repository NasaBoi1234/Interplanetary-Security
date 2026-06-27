# Host Your Discord Bot on Railway (Free 24/7)

Railway is the easiest free option for hosting a Discord bot 24/7. You get $5/month free credit, which is more than enough for a bot.

## Step 1: Prepare Your Bot Files

You need:
- `discord_screening_bot_simple.py` (your bot)
- `requirements.txt` (Python dependencies)
- `.env` (your bot token) - Railway handles this securely
- `Procfile` (tells Railway how to run your bot)
- `runtime.txt` (Python version)

## Step 2: Create Procfile

Create a new file named `Procfile` (no extension):

```
worker: python discord_screening_bot_simple.py
```

This tells Railway to run your bot as a worker (background process).

## Step 3: Create runtime.txt

Create a file named `runtime.txt`:

```
python-3.13.0
```

## Step 4: Update requirements.txt

Make sure your `requirements.txt` has:

```
discord.py>=2.4.0
discord-stubs>=0.1.0
python-dotenv==1.0.0
```

## Step 5: Set Up on Railway

### 5a. Create a Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub (easiest)
3. Authorize Railway to access GitHub

### 5b. Connect Your Repository

**Option A: Push to GitHub (Recommended)**

1. Create a new GitHub repository
2. Add your files:
   - `discord_screening_bot_simple.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `.env.example` (without actual token)
   - `README.md`

3. Push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

**Option B: Deploy Directly (Easier)**

1. Go to [railway.app](https://railway.app/dashboard)
2. Click "New Project"
3. Select "GitHub" and authorize
4. Find and select your repository
5. Click "Deploy"

## Step 6: Add Environment Variables

1. After deploying, go to your Railway project dashboard
2. Click on your deployment
3. Go to "Variables" tab
4. Add:
   - Key: `DISCORD_TOKEN`
   - Value: Your bot token (from Discord Developer Portal)
5. Click "Deploy"

The bot will restart automatically and start running!

## Step 7: Verify It's Running

1. Invite your bot to your Discord server (if not already)
2. In Discord, type: `!ping`
3. Bot should respond with latency

## 🎉 Done!

Your bot is now running 24/7 on Railway for free!

---

# Alternative Free Hosting Options

## Render.com
- **Pros:** Easy setup, good UI
- **Cons:** Free tier spins down after 15 min inactivity (use cron job to keep alive)
- Link: https://render.com

## Oracle Cloud Always Free
- **Pros:** Truly always free, no time limits
- **Cons:** More complex setup, requires credit card
- Link: https://www.oracle.com/cloud/free/

## Replit
- **Pros:** Super easy, built-in editor
- **Cons:** Limited free tier, may get rate limited
- Link: https://replit.com

---

# Monitoring & Uptime

### Optional: Monitor Your Bot

Use **Uptime Robot** (free) to ping your bot every 5 minutes to ensure it stays alive:

1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Create a free account
3. Add Monitor → HTTP(s)
4. URL: `http://localhost:8000` (or your Railway URL if exposed)
5. Interval: 5 minutes

This keeps the bot responsive, though Railway should keep it running anyway.

### Check Logs

In Railway dashboard:
1. Click your deployment
2. Click "Logs" tab
3. See real-time bot activity and errors

---

# Troubleshooting

### Bot won't start
- Check logs in Railway dashboard
- Verify `DISCORD_TOKEN` is correct
- Make sure `requirements.txt` includes all packages

### Bot goes offline after a while
- Railway should keep it running 24/7
- Check if you hit any rate limits (unlikely with this bot)
- Restart the deployment in Railway dashboard

### Environment variables not working
- Make sure variable names match exactly (case-sensitive)
- In Railway, go to Variables and verify they're set
- Redeploy after adding variables

### Costs
- Railway gives you $5/month free
- A Discord bot uses ~0.1-0.5 GB RAM
- Should cost $0 with free tier

---

# That's It!

Your bot is now hosted for free and running 24/7. You can:
- Add new features anytime by updating GitHub
- Railway auto-redeploys when you push changes
- Monitor it from the Railway dashboard
- Never worry about your computer being on

Enjoy! 🎉
