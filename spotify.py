from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

client_id = "674af46cbaf64fb1b7e16782c1e9e73e"
client_secret = "abbba5e52d6f447b911c0039a76dc670"


def get_link(artist, song):
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    link = ''
    title = artist + ' ' + song
    results = sp.search(q=title, type='track', limit=1)
    for i, t in enumerate(results['tracks']['items']):
        link = t['external_urls']['spotify']
    return link
