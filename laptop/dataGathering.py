import math
import random

import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import os
import requests
import re
import datetime
from PIL import Image
from io import BytesIO
import hashing

os.environ['SPOTIPY_CLIENT_ID'] = '3887776ea50a469b81ab216075517bcf'
os.environ['SPOTIPY_CLIENT_SECRET'] = '52bf4482e5ec4256b23b5e6ef6c49a6f'
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


class Artist:
    def __init__(self, name):
        results = sp.search(q=name, type="artist", limit=1)
        self.results = results['artists']['items'][0]
        self.albums = sp.artist_albums(self.get_id())

    def get_name(self):
        return self.results['name']

    def get_followers(self):
        return self.results['followers']['total']

    def get_genres(self):
        return self.results['genres']

    def get_id(self):
        return self.results['id']

    def get_popularity(self):
        return self.results["popularity"]

    def get_spotify_url(self):
        return self.results['uri']

    def get_web_url(self):
        return self.results['external_urls']['spotify']

    def get_top_song(self):
        top_tracks = sp.artist_top_tracks(self.get_id())
        tracks = []
        for i in range(5):
            tracks.append(top_tracks['tracks'][i - 1]['name'])
        return tracks


    def find_intro_paragraphs(self):
        name = f"{self.get_name()}"
        link = "https://en.wikipedia.org/wiki/" + name
        response = requests.get(link)
        paras = []
        if response is not None:
            html = BeautifulSoup(response.text, 'html.parser')
            title = html.select("#firstHeading")[0].text
            paragraphs = html.select("p")
            para = ' '.join([para.text.strip() for para in paragraphs[0:5]])
            paras.append(para)
        return paras

    def get_album_imgs(self):

        album_names = []
        album_ids = [album['id'] for album in self.albums['items'] if album['name'] not in album_names]
        albums = [sp.album(id) for id in album_ids]
        popularity = [album['popularity'] for album in albums]

        sorted_pop = sorted(popularity, reverse=True)[:3]
        popular_albums = [album for popularity, album in zip(popularity, albums) if popularity in sorted_pop]

        image_urls = []
        for album in popular_albums:
            image_urls.append(album['images'][0]['url'])
        return image_urls

    def similar_artists(self):
        related_artists = sp.artist_related_artists(self.get_id())
        artists = []
        for i in related_artists['artists']:
            artists.append(i['name'])
        return artists


class Album:
    def __init__(self, name):
        self.data = sp.search(q=name, type='album', limit=1)['albums']['items'][0]
        self.data2 = sp.album((self.get_id()))
        self.tracks = sp.album_tracks(self.get_id())['items']
        self.artist = sp.artist(self.get_artist_id())

    def get_genres(self):
        return self.artist['genres']

    def get_followers(self):
        return self.artist['followers']['total']

    def get_label(self):
        return self.data2['label']

    def get_name(self):
        return self.data['name']

    def get_id(self):
        return self.data['id']

    def get_tracks(self):
        track_list = []
        for i in self.data2['tracks']['items']:
            track_list.append(i['name'])
        result = ', '.join(track_list)
        return result

    def get_album_length(self):
        duration = sum(track['duration_ms'] for track in self.data2['tracks']['items']) / 3.6e6
        hours, mins = divmod(duration, 1)
        hours = math.floor(hours)
        mins = math.floor(mins * 60)
        if hours:
            return f"{hours} hours and {mins} minutes."
        else:
            return f"{mins} minutes."

    def get_artist(self):
        return self.data['artists'][0]['name']

    def get_artist_id(self):
        return self.data['artists'][0]['id']

    def get_album_image(self):
        return self.data['images'][0]['url']

    def get_popularity(self):
        return self.data2['popularity']

    def get_web_link(self):
        return self.data['external_urls']['spotify']

    def get_release_date(self):
        return self.data['release_date']

    def get_total_tracks(self):
        return self.data['total_tracks']

    def get_mean_audio_feature(self, feature):
        total = 0
        count = 0
        for track in self.tracks:
            audio_features = sp.audio_features(track['id'])[0]
            total += audio_features[feature]
            count += 1
        return total / count

    def get_members(self):
        return self.artist['members']

    def format_info(self):
        data = [f"Date Created: {self.get_release_date()}",
                f"Genres: {self.get_genres()}",
                f"Total Tracks: {self.get_total_tracks()}",
                f"Track Names: {self.get_tracks()}",
                f"Total Length: {self.get_album_length()}"]
        return data

    def get_average_features(self):
        features = ["acousticness", "speechiness", "loudness", "tempo", "valence", "instrumentalness", "danceability",
                    "energy"]
        averages = []
        for feature in features:
            average = self.get_mean_audio_feature(feature)
            averages.append(average)
        rounded_values = [round(value, 2) for value in averages]
        rounded_values[2] += 60
        if rounded_values[3] > 240: rounded_values[3] = 240
        return rounded_values


class Song:
    def __init__(self, name, form):
        if form == "name":
            self.name = name
            self.data = sp.search(q=name, type='track', limit=1)['tracks']['items'][-1]
        elif form == "uri":
            self.data = sp.track(name)
        elif form == "id":
            self.data = sp.track(track_id=name)
        self.audio_features = sp.audio_features(self.data['id'])[0]

    def get_track_name(self):
        return self.data['name']

    def get_track_popularity(self):
        return self.data['popularity']

    def get_track_spotify_web_url(self):
        return self.data['external_urls']['spotify']

    def get_track_id(self):
        return self.data['id']

    def get_artist_name(self):
        return self.data['artists'][0]['name']

    def get_artist_id(self):
        return self.data['artists'][0]['id']

    def get_track_preview_url(self):
        return self.data['preview_url']

    def get_spotify_url(self):
        return self.data['uri']

    def get_album_name(self):
        return self.data['album']['name']

    def get_album_id(self):
        return self.data['album']['id']


    def get_album_image(self):
        get_image_png(self.data['album']['images'][0]['url'], "album1.png")

    # -----

    def get_disc_number(self):
        return self.data['disc_number']

    def get_track_number(self):
        return self.data['track_number']

    def get_release_date(self):
        release = self.data['album']['release_date']
        try:
            date = datetime.datetime.strptime(release, "%Y-%m-%d")
            formatted_date = date.strftime("%d/%m/%Y")
            return formatted_date
        except:
            return release

    def get_year(self):
        return self.get_release_date().split('/')[-1]

    def get_danceability(self):
        return self.audio_features['danceability']

    def get_energy(self):
        return self.audio_features['energy']

    def get_key(self):
        return self.audio_features['key']

    def get_loudness(self):
        return self.audio_features['loudness']

    def get_mode(self):
        return self.audio_features['mode']

    def get_speechiness(self):
        return self.audio_features['speechiness']

    def get_acousticness(self):
        return self.audio_features['acousticness']

    def get_instrumentalness(self):
        return self.audio_features['instrumentalness']

    def get_liveness(self):
        return self.audio_features['liveness']

    def get_valence(self):
        return self.audio_features['valence']

    def get_tempo(self):
        if self.audio_features['tempo'] >= 300: return 300
        else: return self.audio_features['tempo']

    def get_duration_ms(self):
        return self.audio_features['duration_ms']

    def get_time_signature(self):
        return self.audio_features['time_signature']

    def is_explicit(self):
        match self.data['explicit']:
            case True:
                return "TRUE"
            case False:
                return "FALSE"

    def get_genres(self):
        genres = sp.artist(self.get_artist_id())['genres']
        return genres


    def format_string_data(self):
        return [f"Year Released: {self.get_release_date()}       ",
               f"Disc Number : {self.get_disc_number()}         ",
               f"Track Number : {self.get_track_number()}           ",
               f"Popularity : {self.get_track_popularity()}/100         ",
               f"Album : {self.get_album_name()}"]
    def get_hash(self):
        arr = [
            self.get_danceability(),
            self.get_energy(),
            (self.get_key() / 12),
            ((self.get_loudness() + 60) / 60),
            self.get_speechiness(),
            self.get_acousticness(),
            self.get_instrumentalness(),
            self.get_liveness(),
            self.get_valence(),
            (self.get_tempo() / 300)
        ]
        hash_value = hashing.get_hash(arr)
        return hash_value

    def format_data(self):
        return [
            self.get_track_id(),
            self.get_hash()
        ]

    def return_similar(self):
        neighbours = hashing.find_neighbours(self.get_hash(), 2)
        df = pd.read_csv("without repeats.csv")
        matching_tracks = []
        for number in neighbours:
            matching_rows = df[df[' hash'] == number]
            if not matching_rows.empty:
                matching_tracks.extend(matching_rows['track_id'].tolist())
        genres = self.get_genres()
        random.shuffle(matching_tracks)
        similar = []
        names = []
        for song_uri in matching_tracks:
            try:
                current_data = sp.track(song_uri)
                current_genres = sp.artist(current_data['artists'][0]['id'])['genres']
                for genre in current_genres:
                    if genre in genres:
                        if current_data['name'] not in names:
                            print('SUCCESS')
                            similar.append(Song(song_uri,"uri"))
                            names.append(current_data['name'])
                            url = current_data['album']['images'][0]['url']
                            get_image_png(url,f"D:\\Desktop\\COMSPCI NEA\\laptop\\album{len(similar)}.png")

                if len(similar) >= 4: break
            except:
                print("error")

        return similar

    def get_arrray(self):
        arr = [
            self.get_danceability(),
            self.get_energy(),
            (self.get_key() / 12),
            ((self.get_loudness() + 60) / 60),
            self.get_speechiness(),
            self.get_acousticness(),
            self.get_instrumentalness(),
            self.get_liveness(),
            self.get_valence(),
            (self.get_tempo() / 300)
        ]
        return arr


def get_image_png(url, name):
    response = requests.get(url)

    image = Image.open(BytesIO(response.content))

    image.save(name)
