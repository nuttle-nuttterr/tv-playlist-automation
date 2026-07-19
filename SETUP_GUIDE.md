# 🚀 Setup Guide: tv-playlist-automation

Follow these exact steps to get your auto-updating playlist running.

---

## Step 1: Create GitHub Repository

1. Go to **https://github.com/new**
2. **Repository name**: `tv-playlist-automation`
3. **Description**: `Auto-updating Tamil TV playlist combiner`
4. **Visibility**: Public (or Private — Actions work on both)
5. ❌ **UNCHECK** "Add a README file" (we already have one)
6. ❌ **UNCHECK** "Add .gitignore" (we already have one)
7. ❌ **UNCHECK** "Choose a license"
8. Click **Create repository**

---

## Step 2: Push These Files

### Option A: Using setup.sh (Linux/Mac/Git Bash)

```bash
# In this folder, run:
chmod +x setup.sh
./setup.sh

# Then push:
git push -u origin main
```

### Option B: Manual commands

```bash
git init
git add .
git commit -m "Initial commit: TV Playlist Auto-Updater"
git remote add origin https://github.com/nuttle-nuttterr/tv-playlist-automation.git
git push -u origin main
```

### Option C: GitHub Web Upload

1. Download `tv-playlist-automation.zip`
2. Extract it
3. On your GitHub repo page, click **"uploading an existing file"**
4. Drag & drop all files
5. Commit message: `Initial commit`
6. Click **Commit changes**

---

## Step 3: Enable GitHub Actions Permissions

This is **critical** — the workflow needs write access to commit the updated playlist.

1. In your repo, go to **Settings** tab
2. Left sidebar → **Actions** → **General**
3. Scroll to **Workflow permissions**
4. Select ✅ **"Read and write permissions"**
5. Check ✅ **"Allow GitHub Actions to create and approve pull requests"**
6. Click **Save**

---

## Step 4: First Manual Run

1. Go to **Actions** tab
2. Click **"Update M3U Playlist"** workflow
3. Click **"Run workflow"** dropdown → **"Run workflow"**
4. Wait ~1 minute for it to complete
5. Check the **master_playlist.m3u** file — it should now be populated!

---

## Step 5: Verify Auto-Schedule

The workflow is set to run every 6 hours. You don't need to do anything else.

To verify it's scheduled:
1. Go to **Actions** tab
2. Click **"Update M3U Playlist"**
3. Check the schedule badge — it should show the next run time

---

## 📂 File Reference

| File | Purpose |
|------|---------|
| `fetch_and_combine.py` | Main script — fetches, filters, combines |
| `.github/workflows/update-playlist.yml` | GitHub Actions automation |
| `test_validate.py` | Local testing script |
| `requirements.txt` | Python dependencies |
| `setup.sh` | Quick setup helper |
| `README.md` | Project documentation |

---

## 🔄 What Happens Automatically

Every 6 hours, GitHub Actions will:

1. Spin up a fresh Ubuntu runner
2. Install Python + `requests`
3. Run `fetch_and_combine.py`
4. Fetch all 5 source playlists
5. Filter for your wanted channels
6. Remove duplicates
7. Commit `master_playlist.m3u` if changed
8. Log summary to `update_summary.txt`

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Workflow failed" | Check Actions logs → click failed run → read error |
| "No channels found" | Source repos may be down — check URLs manually |
| "Push rejected" | Make sure Actions has Read+Write permissions (Step 3) |
| "Duplicate channels" | Normal — script deduplicates automatically |

---

## 📞 Need Help?

- Check **Actions** tab for run logs
- Read `update_summary.txt` after each run
- Modify `WANTED_CHANNELS` in `fetch_and_combine.py` to add/remove channels
