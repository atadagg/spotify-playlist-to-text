import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def scrape_playlist():
    if request.method == 'POST':
        playlist_url = request.form['playlist_url']
        playlist_id = extract_playlist_id(playlist_url)

        # Use your own Spotify API keys
        client_id = 'client_ID'
        client_secret = 'client_secret'

        # Create a Spotify client
        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Get the playlist tracks
        results = sp.playlist_tracks(playlist_id)
        tracks = results['items']

        playlist_text = ''
        # Iterate through the tracks and get track name and artist name
        for track in tracks:
            if track['track'] is None:  # Skip tracks that have been removed
                continue
            track_name = track['track']['name']
            artist_name = track['track']['artists'][0]['name']
            track_info = f"{track_name} - {artist_name}\n"
            playlist_text += track_info

        return '<pre>' + playlist_text + '</pre>' # Display the playlist tracks <pre> tag preserves whitespace

    return '''
        <form method="post">
            <label for="playlist_url">Enter the Spotify Playlist URL:</label>
            <input type="text" id="playlist_url" name="playlist_url" required>
            <input type="submit" value="Submit">
        </form>
    '''

def extract_playlist_id(playlist_url):
    # Use regex to slice the playlist id
    playlist_id = re.search(r'playlist/([a-zA-Z0-9]+)', playlist_url)
    if playlist_id:
        return playlist_id.group(1)
    else:
        raise ValueError('Invalid playlist URL')

if __name__ == '__main__':
    app.run()
