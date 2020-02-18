#!/usr/bin/env python3

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# TODO: Investigate why decouple isn't working with bare python script
os.environ['SPOTIPY_CLIENT_ID'] = ''
os.environ['SPOTIPY_CLIENT_SECRET'] = ''
os.environ['SPOTIPY_REDIRECT_URI'] = ''

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials())


def get_all_playlist_songs(playlist_id):
    tracks = []
    offset = 0
    repeat = True

    while repeat:
        playlist_data = spotify.playlist_tracks(playlist_id, offset=offset)
        tracks += playlist_data.get('items')
        if not playlist_data.get('next'):
            repeat = False
        else:
            offset += 100
    return tracks


def get_simple_artists_from_track_list(track_list):
    artists = []
    for song in track_list:
        artists += song.get('track').get('artists', [])
    return list({value['name']: value for value in artists}.values())


def get_artist_id_list_from_artist_list(artist_list):
    data = []
    for artist in artist_list:
        if artist.get('id'):
            data.append(artist.get('id'))
    return data


def get_complete_artists_from_artist_list(artist_id_list):
    artists_complete_data = []
    offset = 0
    while offset < len(artist_id_list):
        artists_complete_data += spotify.artists(
            artist_id_list[offset:offset+50]).get('artists')
        offset += 50
    return artists_complete_data


def get_genres_from_artist_list(artist_list):
    genres = []
    for artist in artist_list:
        genres += artist.get('genres', [])
    return list(set(genres))


if __name__ == "__main__":
    ehm_id = '6ealco3hfCp80viBB5iBdX'
    tracks = get_all_playlist_songs(ehm_id)

    print(f'Songs inside Playlist: {len(tracks)}')
    artists_inside_ehm = get_simple_artists_from_track_list(tracks)
    print(
        f'Unique Artists inside Eletro Heart Music Playlist: {len(artists_inside_ehm)}')

    artist_id_list = get_artist_id_list_from_artist_list(artists_inside_ehm)
    complete_artist_list = get_complete_artists_from_artist_list(
        artist_id_list)
    genre_list = get_genres_from_artist_list(complete_artist_list)
    print(f'Genres inside playlist: {len(genre_list)}')
