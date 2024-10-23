import csv
import json
import time

import spotipy
import os
import hashing
from spotipy.oauth2 import SpotifyClientCredentials

os.environ['SPOTIPY_CLIENT_ID'] = '3887776ea50a469b81ab216075517bcf'
os.environ['SPOTIPY_CLIENT_SECRET'] = '52bf4482e5ec4256b23b5e6ef6c49a6f'


def load_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
        return data


def process_playlist(tracks, csv_path):
    sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
    with open(csv_path, 'a', newline='') as f:
        writer = csv.writer(f)
        # Load existing entries into a set
        existing_entries = set()
        if os.path.exists(csv_path):
            with open(csv_path, 'r', newline='') as csv_file:
                reader = csv.reader(csv_file)
                next(reader) # Skip header row
                for row in reader:
                    existing_entries.add(row[0])
        for track in tracks:
            try:
                song_uri = track["track_uri"]
                # Check if entry already exists
                if song_uri not in existing_entries:
                    # Add track ID to existing entries
                    existing_entries.add(song_uri)
                    start = time.time()
                    audio_features = sp.audio_features(song_uri)[0]
                    arr = [
                        audio_features['danceability'],
                        audio_features['energy'],
                        (audio_features['key'] / 12),
                        ((audio_features['loudness'] + 60) / 60),
                        audio_features['speechiness'],
                        audio_features['acousticness'],
                        audio_features['instrumentalness'],
                        audio_features['liveness'],
                        audio_features['valence'],
                        (audio_features['tempo'] / 300)
                    ]
                    song_hash = hashing.get_hash(arr)
                    writer.writerow([song_uri, song_hash])
                    f.flush()
                    end = time.time()
                    print(f"Processed track with URI {song_uri} in playlist, hash is {song_hash}, time taken is {end-start}s")
            except:
                print('sleeping')
                time.sleep(60)

    # sort the csv by hash
    with open(csv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        sorted_rows = sorted(reader, key=lambda x: x[1])
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['track_uri', 'hash'])
        writer.writerows(sorted_rows)


def main(start_index=0):
    directory = "D:\Desktop\COMSPCI NEA\desktop\data"
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            print(filename)
            file_path = os.path.join(directory, filename)
            with open(file_path, "r") as f:
                data = json.load(f)
            playlists = data['playlists']
            for i in range(start_index, len(playlists)):
                playlist = playlists[i]
                tracks = playlist['tracks']
                process_playlist(tracks, "output.csv")
            print("Processing complete!")


if __name__ == '__main__':
    main(0)


