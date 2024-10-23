import os
import json
import dataGathering
import pandas as pd

df = pd.read_csv('tracks_features.csv')

directory = "D:\\Desktop\\COMSPCI NEA\\data\\"

num_files = len(os.listdir(directory))
num_playlists = num_files * 1000
playlist_count = 0

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        file_path = os.path.join(directory, filename)
        with open(file_path, "r") as f:
            data = json.load(f)
        playlists = data['playlists']

        for playlist in playlists:
            playlist_count += 1
            tracks = playlist['tracks']

            for track in tracks:
                track_uri = track['track_uri']
                song = dataGathering.SongForDataset(track_uri,"uri")
                if not df['id'].isin([song.get_track_id()]).any():
                    row_data = song.format_data()
                    new_data = pd.DataFrame([row_data], columns=df.columns)
                    df = pd.concat([df, new_data])
                    df.to_csv('tracks_features.csv', index=False)
            percentage_complete = playlist_count / num_playlists * 100
            print(f"{percentage_complete:.4f}% complete")
