import sqlite3
from sqlite3 import Connection, Cursor
from typing import Any
import os
import spotipy
import spotipy.util as util
import json

def get_spotify_liked() -> dict:
    client_id: str = os.getenv('CLIENT_ID')
    client_secret: str = os.getenv('CLIENT_SECRET')
    redirect_uri: str = os.getenv('REDIRECT_URI')
    username: str = os.getenv("SPOTIFY_USERNAME")
    scope: str = "user-library-read"

    token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id=client_id,
                                   client_secret=client_secret,
                                   redirect_uri=redirect_uri)
    
    more_tracks: bool = True
    response = {}
    i: int = 0

    if token:
        while more_tracks:
            sp = spotipy.Spotify(auth=token)
            results = sp.current_user_saved_tracks(offset=i, limit=50)
            response[i] = results
            i += 50

            if results['next'] is None:
                more_tracks = False

    # with open('liked_songs.json', 'w') as fp:
    #     json.dump(response, fp)

    return response


def main():
    conn: Connection = sqlite3.connect('mixxxdb.sqlite')

    cursor: Cursor = conn.cursor()

    sql_query: str = """
        SELECT PlaylistTracks.position, library.title, library.artist, library.id
        FROM PlaylistTracks
        JOIN library ON PlaylistTracks.track_id = library.id
        WHERE PlaylistTracks.playlist_id = 167
        ORDER BY PlaylistTracks.position;
    """

    cursor.execute(sql_query)
    playlist: list[tuple] = cursor.fetchall()

    for track in playlist:
        print(f"POS: {track[0]}, ID: {track[3]}, NAME: {track[1]}, ARTIST: {track[2]}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    # main()
    spotify_liked: dict = get_spotify_liked()
    print(spotify_liked)
