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
    playlist: list[tuple] = cursor.fetchall()

    for track in playlist:
        print(f"POS: {track[0]}, ID: {track[3]}, NAME: {track[1]}, ARTIST: {track[2]}")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()