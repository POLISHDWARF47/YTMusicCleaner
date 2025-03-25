
# 🎧 YTMusicCleaner
*Clean your YouTube Likes and keep only real music!*

YTMusicCleaner is a simple Python script that filters your **Liked videos** on YouTube and creates a new playlist with only actual music tracks.

---

## 🚀 Features

✅ Filters out **non-music** content (YouTube category ≠ 10)  
✅ Removes **Shorts** (videos under 60 seconds)  
✅ Creates a **clean playlist** with only real tracks  
✅ **Saves progress** to avoid quota errors  
✅ Works across multiple days – safe against YouTube API limits  
✅ Generates **logs** of what's added or skipped

---

## 🛠 Setup Instructions

1. **Enable YouTube Data API v3** in your Google Cloud project  
2. Create OAuth credentials and download your `credentials.json`
3. Clone this repo or [download ZIP](https://github.com/POLISHDWARF47/YTMusicCleaner/archive/refs/heads/main.zip)
4. Run:

```bash
pip install -r requirements.txt
python ytmusic_cleaner.py
```

---

## 📂 Files

| File               | Description                         |
|--------------------|-------------------------------------|
| `ytmusic_cleaner.py` | Main script                        |
| `added_tracks.txt` | Stores IDs of already added tracks  |
| `log.txt`          | Log of added or skipped entries     |
| `requirements.txt` | Python dependencies                 |

---

## 🧠 Notes

- Google API has **daily quota limits** – the script saves your progress so you can run it again tomorrow.
- You can re-run it multiple times safely.

---

## 🙌 Created by

**[@POLISHDWARF47](https://github.com/POLISHDWARF47)**  
Made with ❤️ to fix messy playlists.
