import os
import json
import dataGathering
import csv
import time
import bisect

directory = "D:\\Desktop\\COMSPCI NEA\\desktop\\data\\"
songs_csv_file = 'songs.csv'

last_row_number = 0

if os.path.exists(songs_csv_file):
    with open(songs_csv_file, 'r', newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        # Skip the header row
        next(reader, None)
        # Get the last row number
        for row in reader:
            last_row_number += 1
print(f"Last row number: {last_row_number}")

num_files = len(os.listdir(directory))
num_playlists = num_files * 1000

count = 0
playlist_count = 0
all_songs = []

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
                if track_count <= last_row_number:
                    print(f"Skipping track {track_count} (last row number: {last_row_number})")
                    continue
                start_time = time.time()
                song = dataGathering.SongForDataset(f"{track['track_name']} {track['artist_name']}", "name")
                formatted_song = song.format_data()
                # Insert the song into the sorted list
                position = bisect.bisect_left([s[1] for s in all_songs], formatted_song[1])
                all_songs.insert(position, formatted_song)
                end_time = time.time()
                time_taken = end_time - start_time
                print(f"time taken: {time_taken}, playlist {playlist_count}, track number {track_count}")
                if time_taken > 1:
                    print(f"Skipping track {track_count} because processing time ({time_taken}s) exceeds 1 second")
                    continue

                # Write the song to the CSV file
                with open(songs_csv_file, mode='w', encoding="utf-8", newline='') as file:
                    writer = csv.writer(file)
                    if last_row_number == 0:
                        # Write the header row if this is the first row
                        writer.writerow(["track_id", "hash"])
                        last_row_number += 1
                    writer.writerows(all_songs)