import os
import json
import dataGathering
import time
import pandas as pd

directory = "D:\\Desktop\\COMSPCI NEA\\data\\"
songs_csv_file = 'songs.csv'

if os.path.exists(songs_csv_file):
    df = pd.read_csv(songs_csv_file)
else:
    df = pd.DataFrame(columns=["track_id", "hash"])
    # Write the header row
    df.to_csv(songs_csv_file, index=False)

num_files = len(os.listdir(directory))
num_playlists = num_files * 1000

count = 0
playlist_count = 0

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        print(filename)
        file_path = os.path.join(directory, filename)
        with open(file_path, "r") as f:
            data = json.load(f)
        playlists = data['playlists']
        track_count = 0

        for playlist in playlists:
            playstart = time.time()
            playlist_count += 1
            tracks = playlist['tracks']
            print(f"New playlist: {playlist_count}")
            for track in tracks:
                track_count += 1
                # Skip tracks that have already been processed
                if track_count <= len(df):
                    print(f"Skipping track {track_count} (last row number: {len(df)})")


                    continue
                start_time = time.time()
                song = dataGathering.SongForDataset(track['track_uri'], "uri")
                formatted_song = song.format_data()
                song_df = pd.DataFrame([formatted_song], columns=["track_id", "hash"])
                idx = df[df['hash'] > formatted_song[1]].index.min()
                if pd.isna(idx):
                    df = df.append(song_df, ignore_index=True)
                else:
                    df = pd.concat([df.iloc[:idx], song_df, df.iloc[idx:]]).reset_index(drop=True)

                # Write the updated DataFrame to the CSV file
                df.to_csv(songs_csv_file, index=False)

                end_time = time.time()
                print(f"time taken: {end_time-start_time}, playlist {playlist_count}, track number {track_count}")

            play_end = time.time()
            print(f"\nPlaylist processed in {play_end-playstart}, {round((playlist_count/num_playlists) * 100,4)}% processed\n")
