#python bot.py
import json
import os

SONGS_FILE = "songs.json"


def load_songs():
    if not os.path.exists(SONGS_FILE):
        return {"songs": [], "last_id": 0}

    with open(SONGS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_songs(data):
    with open(SONGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_song(song_data):
    data = load_songs()
    data["last_id"] += 1
    song_data["id"] = data["last_id"]
    data["songs"].append(song_data)
    save_songs(data)
    return song_data["id"]