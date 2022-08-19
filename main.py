import os
import json
from ytmusicapi import YTMusic
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SongInfo:
    def __init__(self, title, artists, album):
        self.title = title
        self.artists = artists
        self.album = album

    def __repr__(self):
        return f'"{self.title}" by {self.artists} in album "{self.album}"'


def prettyPrint(jsonData):
    print(json.dumps(
        jsonData,
        sort_keys=False,
        indent=4,
        separators=(',', ': ')
    ))

# Retrieve config data


f = open('config.json')
data = json.load(f)

clientID = data["clientID"]
clientSecret = data["clientSecret"]
userID = data["userID"]
oldPlaylistID = data["oldPlayListID"]

# Get all tracks from matching YT Music Playlist

client = YTMusic('headers_auth.json')
retrievedPlaylist = client.get_playlist(oldPlaylistID)
prettyPrint(retrievedPlaylist)

playlistTitle = retrievedPlaylist['title']
description = retrievedPlaylist["description"]
retrievedTrackList = retrievedPlaylist["tracks"]

createdTrackList = []
for i in range(0, len(retrievedTrackList)):
    track = retrievedTrackList[i]
    title = track["title"]
    artistsArray = track["artists"]

    artists = []
    for i in range(0, len(artistsArray)):
        artistInfo = artistsArray[i]
        artists.append(artistInfo["name"])

    albumInfo = track["album"]
    album = albumInfo if albumInfo == None else albumInfo["name"]
    newSong = SongInfo(title, artists, album)
    createdTrackList.append(newSong)

print(createdTrackList)

# Spotify playlist creation

os.environ["SPOTIPY_CLIENT_ID"] = clientID
os.environ["SPOTIPY_CLIENT_SECRET"] = clientSecret
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost:3000/"
scope = "playlist-modify-public"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Create

res = sp.user_playlist_create(
    user=userID, name=playlistTitle, public=True, collaborative=False, description=description)
prettyPrint(res)

playlistID = res["id"]
print("Playlist Created With ID ", playlistID)

trackIDs = []
# Add each matching song
for i in range(0, len(createdTrackList)):
    track = createdTrackList[i]

    # Title, artists, album
    q = f"track:{track.title}"

    res = sp.search(q=q, type="track")
    prettyPrint(res)

    allTracks = res["tracks"]["items"]
    found = False
    for i in range(0, len(allTracks)):
        curTrack = allTracks[i]
        for j in range(0, len(curTrack["artists"])):
            curArtist = curTrack["artists"][j]["name"]
            for k in range(0, len(track.artists)):
                print(curArtist, track.artists[k])
                if curArtist == track.artists[k]:
                    print("yes")
                    trackIDs.append(curTrack["id"])
                    found = True
                    break
                print("no")
            if found:
                break
        if found:
            break

    # if not found:
    #     print(f'No search result matched for {q}')

res = sp.playlist_add_items(playlist_id=playlistID, items=trackIDs)
prettyPrint(res)
