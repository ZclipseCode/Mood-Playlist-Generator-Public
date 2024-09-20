import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# ID and SECRET should be kept secret
os.environ["SPOTIPY_CLIENT_ID"] = ""
os.environ["SPOTIPY_CLIENT_SECRET"] = ""
os.environ["SPOTIPY_REDIRECT_URI"] = "http://localhost/"

# change username
SCOPE = "playlist-modify-public playlist-modify-private"
USERNAME = ""
TOKEN = SpotifyOAuth(scope=SCOPE, username=USERNAME)
SPOTIFY = spotipy.Spotify(auth_manager=TOKEN)

def Options():
    option = ""

    while option != "1" and option != "2" and option != "3":
        print("What would you like to do? (Enter a number.)")
        print("1. Create new mood playlist")
        print("2. Add songs to existing playlist")
        print("3. Exit")

        option = input()

        print()
    
    if option == "1":
        CreateNewMoodPlaylist()
    elif option == "2":
        AddToExistingPlaylist()
    elif option == "3":
        print("Enjoy the music!")

def AddTrack():
    option = ""
    optionNum = -1

    search = input("Input the name of a track you would like to base the mood playlist off of: ")
    results = SPOTIFY.search(q="track:" + search, type="track,artist")
    tracks = results["tracks"]["items"]

    print()

    while not option.isnumeric() or optionNum > len(tracks) or optionNum <= 0:
        print("Select a track. (Enter a number.)")

        for x in range(len(tracks)):
            print(f"{x + 1}.", tracks[x]["name"], "by", tracks[x]["artists"][0]["name"])

        option = input()

        if (option.isnumeric()):
            optionNum = int(option)
        
        print()

    return tracks[optionNum - 1]

def CreateNewMoodPlaylist():
    tracks = []
    additionalTracksStr = ""
    additionalTracks = -1

    for x in range(3):
        tracks.append(AddTrack())

    # reccomendations() limits to 100
    while not additionalTracksStr.isnumeric() or additionalTracks <= 0 or additionalTracks > 97:
        additionalTracksStr = input("Input the amount of additional tracks to add to the playlist (between 1 - 97): ")

        if additionalTracksStr.isnumeric():
            additionalTracks = int(additionalTracksStr)
        
        print()
    
    seedTrackIds = [track["id"] for track in tracks]
    recommendations = SPOTIFY.recommendations(seed_tracks=seedTrackIds, limit=additionalTracks)
    recommendedTracks = recommendations["tracks"]

    print("Here is your playlist:")

    for z in range(len(tracks)):
        print(f"{z + 1}.", tracks[z]["name"], "by", tracks[z]["artists"][0]["name"])

    for y in range(len(recommendedTracks)):
        print(f"{z + 1 + y + 1}.", recommendedTracks[y]["name"], "by", recommendedTracks[y]["artists"][0]["name"])
    
    print()

    playlistName = ""

    while len(playlistName) <= 0:
        playlistName = input("Input a name for the playlist: ")

        print()
    
    userId = SPOTIFY.current_user()["id"]
    playlist = SPOTIFY.user_playlist_create(user=userId, name=playlistName, public=True, description="Created with the Mood Playlist Generator by Brian Michael")
    
    trackUris = []
    for a in range(len(tracks)):
        trackUris.append(tracks[a]["uri"])
    for b in range(len(recommendedTracks)):
        trackUris.append(recommendedTracks[b]["uri"])

    SPOTIFY.playlist_add_items(playlist["id"], trackUris)

    print(f"\033[32m{playlistName} playlist created! You can find it here:\033[0m")
    print(f"\033[32m{playlist['external_urls']['spotify']}\033[0m")

    print()

    Options()

def AddToExistingPlaylist():
    playlist = ""

    link = input("Input a link to a playlist you would like to add to: ")
    
    print()

    try:
        playlist = SPOTIFY.playlist(link)
    except:
        print("\033[31mInvalid playlist link!\033[0m")

        print()

        AddToExistingPlaylist()

    playlist = SPOTIFY.playlist(link)
    tracks = SPOTIFY.playlist_tracks(playlist["id"])["items"]

    print(playlist["name"], "found! Here are its tracks:")

    for x in range(len(tracks)):
        print(f"{x + 1}.", tracks[x]["track"]["name"], "by", tracks[x]["track"]["artists"][0]["name"])
    
    print()

    additionalTracksStr = ""
    additionalTracks = -1

    # reccomendations() limits to 100
    while not additionalTracksStr.isnumeric() or additionalTracks <= 0 or additionalTracks > 97:
        additionalTracksStr = input("Input the amount of additional tracks to add to the playlist (between 1 - 97): ")

        if additionalTracksStr.isnumeric():
            additionalTracks = int(additionalTracksStr)
        
        print()
    
    seedTrackIds = [track["track"]["id"] for track in tracks]
    recommendations = SPOTIFY.recommendations(seed_tracks=seedTrackIds, limit=additionalTracks)
    recommendedTracks = recommendations["tracks"]

    tracksToAdd = [track["id"] for track in recommendedTracks]
    SPOTIFY.user_playlist_add_tracks(SPOTIFY.current_user()["id"], playlist["id"], tracksToAdd)

    print(f"\033[32m{playlist['name']} updated!\033[0m")

    print()

    print("Here is your new playlist:")

    for z in range(len(tracks)):
        print(f"{z + 1}.", tracks[z]["track"]["name"], "by", tracks[z]["track"]["artists"][0]["name"])

    for y in range(len(recommendedTracks)):
        print(f"{z + 1 + y + 1}.", recommendedTracks[y]["name"], "by", recommendedTracks[y]["artists"][0]["name"])
    
    print()

    print("\033[32mYou can find it here:\033[0m")
    print(f"\033[32m{playlist['external_urls']['spotify']}\033[0m")

    print()

    Options()

def main():

    print("Welcome to the Mood Playlist Generator by Brian Michael")

    print()

    Options()

main()