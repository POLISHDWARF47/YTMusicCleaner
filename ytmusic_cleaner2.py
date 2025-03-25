from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os
import isodate
from datetime import datetime

SCOPES = ["https://www.googleapis.com/auth/youtube"]

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=creds)

def get_liked_videos(youtube):
    videos = []
    nextPageToken = None
    while True:
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            playlistId="LL",
            pageToken=nextPageToken
        )
        response = request.execute()
        for item in response["items"]:
            video_id = item["contentDetails"]["videoId"]
            title = item["snippet"]["title"]
            videos.append((video_id, title))
        nextPageToken = response.get("nextPageToken")
        if not nextPageToken:
            break
    return videos

def filter_music_videos(youtube, videos):
    music_ids = []
    short_count = 0
    for vid_id, title in videos:
        try:
            req = youtube.videos().list(part="snippet,contentDetails", id=vid_id)
            res = req.execute()
            if res["items"]:
                item = res["items"][0]
                categoryId = item["snippet"]["categoryId"]
                duration = isodate.parse_duration(item["contentDetails"]["duration"]).total_seconds()
                if categoryId == "10" and duration > 60:
                    music_ids.append(vid_id)
                elif categoryId == "10" and duration <= 60:
                    short_count += 1
        except Exception as e:
            log(f"[BŁĄD] przy sprawdzaniu {vid_id}: {e}")
    return music_ids, short_count

def create_playlist(youtube, title="Polubione Piosenki"):
    req = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title},
            "status": {"privacyStatus": "private"}
        }
    )
    res = req.execute()
    return res["id"]

def load_added_ids():
    if not os.path.exists("added_tracks.txt"):
        return set()
    with open("added_tracks.txt", "r") as f:
        return set(line.strip() for line in f.readlines())

def save_added_id(video_id):
    with open("added_tracks.txt", "a") as f:
        f.write(video_id + "\n")

def log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")
    print(message)

def add_to_playlist(youtube, playlist_id, video_ids):
    added_ids = load_added_ids()
    count = 0
    for vid in video_ids:
        if vid in added_ids:
            continue
        try:
            youtube.playlistItems().insert(
                part="snippet",
                body={
                    "snippet": {
                        "playlistId": playlist_id,
                        "resourceId": {
                            "kind": "youtube#video",
                            "videoId": vid
                        }
                    }
                }
            ).execute()
            save_added_id(vid)
            log(f"[OK] Dodano: {vid}")
            count += 1
        except Exception as e:
            log(f"[STOP] quota exceeded lub inny błąd przy {vid}: {e}")
            break
    log(f"[INFO] Dodano {count} nowych utworów do playlisty.")

def main():
    youtube = authenticate()
    liked = get_liked_videos(youtube)
    log(f"[INFO] Znaleziono {len(liked)} polubionych filmów")

    music, short_count = filter_music_videos(youtube, liked)
    log(f"[INFO] Znaleziono {len(music)} muzycznych utworów (>60s)")
    log(f"[INFO] Shortów (<=60s): {short_count}")

    playlist_id = create_playlist(youtube)
    log("[INFO] Tworzenie playlisty...")

    add_to_playlist(youtube, playlist_id, music)
    log("[INFO] Gotowe!")

if __name__ == "__main__":
    main()
