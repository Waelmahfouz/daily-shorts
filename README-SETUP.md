# Daily auto-video on GitHub (free)

This makes **one short video per day** in your chosen niche, automatically, on
GitHub's servers — nothing runs on your laptop. Each day it picks a fresh topic
(using your free Groq key), builds the video (Pexels clips + free voice), and
saves the finished **MP4 + a suggested title/caption** for you to download and
post to TikTok / YouTube yourself.

Cost: **$0.** GitHub Actions is free for this, Groq is free, Pexels is free.

---

## One-time setup (about 10 minutes)

### 1. Create a free GitHub account
Go to https://github.com and sign up if you don't have one.

### 2. Create a new repository
- Click the **+** (top right) → **New repository**.
- Name it anything, e.g. `daily-shorts`.
- Set it to **Private**.
- Click **Create repository**.

### 3. Upload these files into the repo
On the new repo page, click **"uploading an existing file"**, then drag in
**all** the files/folders from this package, keeping the structure:

```
.github/workflows/daily-video.yml
scripts/pick_topic.py
niche.txt
README-SETUP.md
```

Then click **Commit changes**.

> If drag-and-drop won't keep the `.github/workflows/` folder, use
> **Add file → Create new file**, type the path
> `.github/workflows/daily-video.yml` in the name box, and paste the contents
> of that file. Do the same for `scripts/pick_topic.py`.

### 4. Add your two secret keys
In the repo: **Settings → Secrets and variables → Actions → New repository secret.**
Add these two (names must match exactly):

| Name             | Value                          |
|------------------|--------------------------------|
| `GROQ_API_KEY`   | your Groq key (starts `gsk_`)  |
| `PEXELS_API_KEY` | your Pexels key                |

### 5. Set your niche
Open `niche.txt` in the repo (click it → pencil icon), replace the last line
with your niche, and **Commit**. You can list several niches (one per line) to
rotate through them.

### 6. Turn it on and test
- Go to the **Actions** tab → if prompted, click **"I understand… enable"**.
- Click **Daily Short Video** → **Run workflow** → **Run workflow** (this runs it
  once now, so you don't have to wait for tomorrow).
- When it finishes (a few minutes), open the run and download the
  **daily-video-… artifact** at the bottom. Inside: your `video_1.mp4` and
  `post-text.txt` (title + caption).

That's it. From now on it runs by itself every day.

---

## Everyday use
- **Change topics:** edit `niche.txt`.
- **Force a specific topic once:** Actions → Run workflow → type it in the
  "topic override" box.
- **Change the time:** edit the `cron` line in `daily-video.yml`
  (it's in UTC; 06:00 UTC = 09:00 Beirut).

## Good to know
- GitHub **pauses scheduled jobs after ~60 days with no activity** in the repo.
  Just make any small commit occasionally (e.g. tweak `niche.txt`) to keep it alive.
- Want auto-posting later instead of manual? That needs Upload-Post.com
  (free = ~10 posts/month, or $16/month unlimited). Ask and I'll wire it in.
