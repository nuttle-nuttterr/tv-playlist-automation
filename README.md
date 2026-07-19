# 📺 TV Playlist Auto-Updater

Automatically fetches, filters, combines, and deduplicates Tamil local TV channel playlists from multiple GitHub sources every **6 hours**.

---

## 🚀 How It Works

| Step | Description |
|------|-------------|
| **1. Fetch** | Downloads M3U playlists from 5 source repositories |
| **2. Filter** | Keeps only working local Tamil channels (300+ curated) |
| **3. Deduplicate** | Removes duplicate channels by name & URL |
| **4. Sort** | Alphabetically sorts all channels |
| **5. Publish** | Commits updated `master_playlist.m3u` to this repo |

---

## 📡 Source Repositories

| # | Repository | Branch/File |
|---|-----------|-------------|
| 1 | `nuttle-nuttterr/Mk-tholaikaatchi-test` | `main/master_playlist.m3u` |
| 2 | `nuttle-nuttterr/Ds2` | `main/playlist.m3u` |
| 3 | `nuttle-nuttterr/tv-by-Gemini` | `main/master_playlist.m3u` |
| 4 | `nuttle-nuttterr/tv-by-deepseek` | `main/master_playlist.m3u` |
| 5 | `nuttle-nuttterr/Tv-by-Claude` | `main/master_playlist.m3u` |

---

## 📂 Output Files

| File | Description |
|------|-------------|
| `master_playlist.m3u` | Combined, filtered, deduplicated playlist |
| `update_summary.txt` | Last update log with channel count |

---

## ⏰ Update Schedule

Runs automatically via GitHub Actions every **6 hours**:
- `00:00 UTC`
- `06:00 UTC`
- `12:00 UTC`
- `18:00 UTC`

You can also trigger manually via **Actions → Update M3U Playlist → Run workflow**.

---

## 🛠 Local Usage

```bash
# Clone the repo
git clone https://github.com/nuttle-nuttterr/tv-playlist-automation.git
cd tv-playlist-automation

# Install dependency
pip install requests

# Run the script
python fetch_and_combine.py
```

---

## 📋 Included Channel Categories

- ✅ Tamil Local Channels
- ✅ News Channels (Polimer, Thanthi, News7, etc.)
- ✅ Entertainment (Zee Tamil, Kalaignar, Raj TV, etc.)
- ✅ Sports (Star Sports, Sony Sports, Eurosport)
- ✅ Movies (J Movie, Roja Movies, Tharun Movies, etc.)
- ✅ Music (Isaiaruvi, SS Music, Vinmeen Music, etc.)
- ✅ Kids (Disney Channel, Nickelodeon, etc.)
- ✅ Devotional/Religious channels
- ✅ Regional local channels

---

## ⚙️ Customization

Edit `fetch_and_combine.py` to:
- Add/remove source URLs (`SOURCE_URLS`)
- Add/remove wanted channels (`WANTED_CHANNELS`)
- Change update frequency (`.github/workflows/update-playlist.yml` cron schedule)

---

## 📝 License

This project is for personal/educational use. Channel streams belong to their respective owners.
