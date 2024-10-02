import sqlite3
from sqlite3 import Connection, Cursor
from typing import Any

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
    playlists: list[tuple] = cursor.fetchall()

    print("All Playlists in the Mixxx database:")
    for playlist in playlists:
        print(f"Position: {playlist[0]}, Name: {playlist[1]}, Artiist: {playlist[2]}, ID: {playlist[3]}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()