import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
import os
import requests
import re
import hash
os.environ['SPOTIPY_CLIENT_ID'] = '6785384b895f462abd087b76d25e6f88'
os.environ['SPOTIPY_CLIENT_SECRET'] = 'f6a88c1ef0a04210b713a3a061867d71'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def find_info(name):
    artist = Artist(name)
    link = "https://en.wikipedia.org/w/index.php?search=" + artist.get_name() + " artist" + "&title=Special%3ASearch&fulltext=1&ns0=1"

    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a', href=True)

    hrefs = []
    for i in links: hrefs.append(i['href'])

    new_link = "https://en.wikipedia.org/" + str(hrefs[9])
    response = requests.get(new_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    paras = soup.find_all('p')
    long_paras = []
    for i in paras:
        if len(i.get_text()) > 100:
            long_paras.append(i.get_text())
    print(long_paras[0])

    print(long_paras)
    print(new_link)


class Artist:
    def __init__(self, name):
        results = sp.search(q=name, type="artist", limit=1)
        self.results = results['artists']['items'][0]

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

        return top_tracks['tracks'][0]['name']

    def get_info_box(self):
        link = "https://en.wikipedia.org/w/index.php?search=" + self.get_name() + " artist" + "&title=Special%3ASearch&fulltext=1&ns0=1"

        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        hrefs = []
        for i in links: hrefs.append(i['href'])

        new_link = "https://en.wikipedia.org/" + str(hrefs[9])
        response = requests.get(new_link)
        soup = BeautifulSoup(response.text, 'html.parser')

        info_box = soup.find('table', {'class': 'infobox'})

        info_box_data = {}
        rows = info_box.find_all('tr')
        for row in rows:
            key = row.find('th')
            value = row.find('td')

            if key and value:
                key = key.get_text().strip()
                value = value.get_text().strip()

                key = re.sub(r'\s+', ' ', key)
                value = re.sub(r'\s+', ' ', value)

                info_box_data[key] = value

        print(info_box_data)

    def find_intro_paragraphs(self):
        link = "https://en.wikipedia.org/w/index.php?search=" + self.get_name() + " artist" + "&title=Special%3ASearch&fulltext=1&ns0=1"

        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        hrefs = []
        for i in links: hrefs.append(i['href'])

        new_link = "https://en.wikipedia.org/" + str(hrefs[9])
        response = requests.get(new_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        paras = soup.find_all('p')

        intro_para = paras[0]
        intro_text = [intro_para.get_text()]

        toc = soup.find('div', {'id': 'toc'})

        while intro_para and intro_para != toc:
            intro_text.append(intro_para.get_text())
            intro_para = intro_para.find_next_sibling('p')

        intro_text = intro_text[:-3]

        intro_text = [re.sub(r'\[[^\]]*\]', '', p) for p in intro_text]
        intro_text = [p.replace('\n', '') for p in intro_text]
        intro_text = [p for p in intro_text if p]
        return intro_text


class Album:
    def __init__(self, name):
        self.data = sp.search(q=name, type='album', limit=1)['albums']['items'][0]

    def get_name(self):
        return self.data['name']

    def get_id(self):
        return self.data['id']

    def get_artist(self):
        return self.data['artists'][0]['name']

    def get_artist_id(self):
        return self.data['artists'][0]['id']

    def get_album_image(self):
        return self.data['images'][0]['url']

    def get_web_link(self):
        return self.data['external_urls']['spotify']


class Song:
    def __init__(self, name, form):
        if form == "name":
            self.name = name
            self.data = sp.search(q=name, type='track', limit=1)['tracks']['items'][-1]
        elif form == "uri":
            self.data = sp.track(name)
        elif form == "id":
            self.data = sp.track(track_id=name)

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


class SongForDataset(Song):
    def __init__(self, name, form):
        super(SongForDataset, self).__init__(name, form)
        self.audio_features = sp.audio_features(self.data['id'])[0]

    def get_artist_name(self):
        return [artist['name'] for artist in self.data['artists']]

    def get_artist_id(self):
        return [artist['id'] for artist in self.data['artists']]

    # -----

    def get_disc_number(self):
        return self.data['disc_number']

    def get_track_number(self):
        return self.data['track_number']

    def get_release_date(self):
        try:
            release = self.data['album']['release_date']
            return release
        except:
            return self.data['album']['release_date']

    def get_year(self):
        return int(self.get_release_date().split('-')[0])

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
        return self.audio_features['tempo']

    def get_duration_ms(self):
        return self.audio_features['duration_ms']

    def get_time_signature(self):
        return self.audio_features['time_signature']

    def is_explicit(self):
        if self.data['explicit']:
            return "True"
        else:
            return "False"

    def get_hash(self):
        return hash.get_hash([
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
            ])

    def format_data(self):
        return [self.get_track_id(),
                self.get_hash()
        ]
