import pafy, spotipy, configparser, json, time, re
from spotipy.oauth2 import SpotifyOAuth

config = configparser.ConfigParser()
config.read('config.cfg')
username = config.get('SPOTIFY', 'USERNAME')
client_id = config.get('SPOTIFY', 'CLIENT_ID')
client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
scope = 'playlist-modify-public'

token = spotipy.util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost/") 
sp = spotipy.Spotify(auth=token)

YoutubeAPIKey = config.get('SPOTIFY','YOUTUBE_API_KEY')
pafy.set_api_key(YoutubeAPIKey)

def getYoutubePlaylistTitle(url):
    playlist = pafy.get_playlist2(url)
    # print(playlist.title)
    return playlist.title

def getYouTitles(url):
    playlist = pafy.get_playlist2(url)
    playlistTitles = []
    #print(playlist.title)
    try:
        for i in range(len(playlist)):
            #print("index: ", i)
            #print(playlist[i].title)
            playlistTitles.append(playlist[i].title)
    except:
        print('error iterating through titles in playlist! Check for deleted or missing videos in playlist')

    for i in range(len(playlistTitles)):
        #print("before ", titles)
        playlistTitles[i] = re.sub("[\(\[].*?[\)\]]", "", playlistTitles[i])
        playlistTitles[i] = re.sub('lyrics', '', playlistTitles[i], flags=re.IGNORECASE)
        #print("after ", titles)

    return playlistTitles

def getPlaylistID(playlistName):
    playlist_id = ''
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:  # iterate through playlists I follow
        if playlist['name'] == playlistName:  # filter for newly created playlist
            playlist_id = playlist['id']
    return playlist_id

def createSpotPlaylist(url, playlistName, playlistDescrip):
    sp.user_playlist_create(username, name=playlistName, public=True, collaborative=False, description=playlistDescrip)
    time.sleep(2)
    playlistTitles = getYouTitles(url)
    trackIds = getTrackIds(playlistTitles)
    playlistId = getPlaylistID(playlistName)
    sp.user_playlist_add_tracks(username, playlistId, trackIds)

def getTrackIds(playlistTitles):
    track_ids = []
    for title in playlistTitles:
        results = sp.search(q=f"{title} ", type='track')
        if results['tracks']['total'] == 0: #if track isn't on spotify as queried, go to next track
            print("Unable to add", title)
            continue
        else:
            track_ids.append(results['tracks']['items'][0]['id'])

    return track_ids

def readSpotPlaylists():
    userPlaylists = sp.user_playlists(username, limit=50, offset=0)

    with open('info.json', 'w') as outfile:
        json.dump(userPlaylists, outfile)

    userPlaylistsTitles = []
    for item in userPlaylists['items']:
        userPlaylistsTitles.append(item['name'])
    
    return userPlaylistsTitles

spotPlaylistTitles = readSpotPlaylists()
print()
print("BEFORE USING:")
print("Clear the youtube playlist of any deleted/removed videos")
print()
playlistURL = input("Enter the url of the Youtube Playlist: ")
nameCheck = True
while nameCheck:
    nameChoice = input("Do you want the playlist to be named the same as the Youtube Playlist? (Y/N) ")
    if (nameChoice == 'Y' or nameChoice == 'y'):
        playlistName = getYoutubePlaylistTitle(playlistURL)
        if playlistName in spotPlaylistTitles:
            print("There is already a playlist in your library named,", playlistName, ", enter a different name")
            nameCheck = False
        else:
            break
    elif (nameChoice == 'N' or nameChoice == 'n'):
        while True:
            playlistName = input("Enter the name for the playlist to be created: ")
            if playlistName in spotPlaylistTitles:
                print("There is already a playlist in your library named,", playlistName,", enter a different name")
            else:
                break
        break
    else:
        print("Invalid choice")

if (nameCheck == False):
    while True:
        playlistName = input("Enter the name for the playlist to be created: ")
        if playlistName in spotPlaylistTitles:
            print("There is already a playlist in your library named,", playlistName, ", enter a different name")
        else:
            break

while True:
    descripChoice = input("Do you want a playlist description? (Y/N) ")
    if (descripChoice == 'Y' or descripChoice == 'y'):
        playlistDescrip = input("Enter a description: ")
        break
    elif (descripChoice == 'N' or descripChoice == 'n'):
        playlistDescrip = 'This playlist was made by a program'
        break
    else:
        print("Invalid choice")
    
print()
createSpotPlaylist(playlistURL, playlistName, playlistDescrip)

print()
e = input("Press any button to close")
#pyinstaller main.py --name YoutubeToSpotify --add-data config.cfg;.