import pafy, spotipy, configparser, json
from spotipy.oauth2 import SpotifyOAuth

def getYouTitles():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    YoutubeAPIKey = config.get('SPOTIFY','YOUTUBE_API_KEY')
    pafy.set_api_key(YoutubeAPIKey)
    url = "https://www.youtube.com/playlist?list=PLESVm2hBvzZHFsfGYo6Q6eyXshzhBLTBK"
    playlist = pafy.get_playlist2(url)
    try:
        for i in range(len(playlist)):
            #print("index: ", i)
            print(playlist[i].title)
    except:
        print('error iterating through titles in playlist! Check for deleted or missing videos in playlist')

def createSpotPlaylist():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    username = config.get('SPOTIFY', 'USERNAME')
    client_id = config.get('SPOTIFY', 'CLIENT_ID')
    client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
    scope = 'playlist-modify-public'


    token = spotipy.util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost/") 
    sp = spotipy.Spotify(auth=token)
    sp.user_playlist_create(username, name='Python Made Me', public=True, collaborative=False, description="This playlist was made by a program for testing purposes")

def readSpotPlaylists():
    config = configparser.ConfigParser()
    config.read('config.cfg')
    username = config.get('SPOTIFY', 'USERNAME')
    client_id = config.get('SPOTIFY', 'CLIENT_ID')
    client_secret = config.get('SPOTIFY', 'CLIENT_SECRET')
    scope = 'playlist-read-private'


    token = spotipy.util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost/") 
    sp = spotipy.Spotify(auth=token)
    userPlaylists = sp.user_playlists(username, limit=50, offset=0)

    #with open('info.json', 'w') as outfile:
    #    json.dump(userPlaylists, outfile)

    userPlaylistsTitles = []
    for item in userPlaylists['items']:
        userPlaylistsTitles.append(item['name'])
    
    print(userPlaylistsTitles)
    
createSpotPlaylist()