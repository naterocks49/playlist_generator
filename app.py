import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, redirect, url_for, render_template, request, session
from dotenv import load_dotenv  # Import the load_dotenv function
import os

load_dotenv()  # Load environment variables from .env file


app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET')

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')


sp_oauth = SpotifyOAuth(
    SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, scope='playlist-modify-public'
)

@app.route('/')
def index():
    artists = ["Mac miller", "J Cole", "Kanye West"]
    token_info = session.get('token_info')
    if token_info is None:
        return redirect(url_for('login'))
    return render_template('index.html', artists=artists)

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return render_template('login.html', auth_url=auth_url)

@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info
    return redirect(url_for('index'))

@app.route('/create_playlist')
def create_playlist():
    token_info = session.get('token_info')
    if token_info is None:
        return redirect(url_for('login'))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_info = sp.me()
    playlist_name = "My Awesome Playlist"
    playlist_description = "An automatically created playlist by the Spotify Playlist App"
    sp.user_playlist_create(user_info['id'], playlist_name, public=True, description=playlist_description)
    
    return "Playlist created!"

if __name__ == '__main__':
    app.run(debug=True)
