import spotipy
from spotipy.oauth2 import SpotifyOAuth
import lyricsgenius
import openai
import os
import time
import firebase_admin
from firebase_admin import credentials, firestore
import datetime

cred = credentials.Certificate("vigama-ai-hacks-firebase-adminsdk-5waoy-7ddd5ba925.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOT_CLIENT_ID'),
                                               client_secret=os.getenv('SPOT_CLIENT_SECRET'),
                                               redirect_uri='http://localhost:8000/callback',
                                               scope='user-read-recently-played'))

# Set up authentication for Genius API
genius_token =os.getenv('GENIUS_TOKEN')
genius = lyricsgenius.Genius(genius_token)

# Set up authentication for OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')


def fetch_uno():
    results = sp.current_user_recently_played(limit=1)
    for item in results['items']:
        track = item['track']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        # Look up lyrics using Genius API
        song = genius.search_song(track_name, artist_name)
        if song is None:
            continue
    
        lyrics = song.lyrics
        lyrics_compressed = lyrics[:len(lyrics) // 10]
        # Analyze sentiment using OpenAI API
        prompt = f"The song '{track_name}' by {artist_name} goes like this:\n\n{lyrics_compressed}\n\n"
        prompt += "What sentiment does this song convey?Answer Negative positive or neutral only, add no period"
        response = openai.Completion.create( 
            engine='text-davinci-003',
            prompt=prompt,
            temperature=0.3
        )

        sentiment = response.choices[0].text.strip()

    # Determine general consensus
        return sentiment

    #return track_name = track['name']
def fetch_n_find(results):
    sad_score =0
    for item in results['items']:
        track = item['track']
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        # Look up lyrics using Genius API
        song = genius.search_song(track_name, artist_name)
        if song is None:
            continue
    
        lyrics = song.lyrics
        lyrics_compressed = lyrics[:len(lyrics) // 10]
        # Analyze sentiment using OpenAI API
        prompt = f"The song '{track_name}' by {artist_name} goes like this:\n\n{lyrics_compressed}\n\n"
        prompt += "What sentiment does this song convey?Answer Negative positive or neutral only, add no period"
        response = openai.Completion.create( 
            engine='text-davinci-003',
            prompt=prompt,
            temperature=0.3
        )

        sentiment = response.choices[0].text.strip()

    # Determine general consensus
        threshold = 0.5  

        if sentiment.lower() == 'negative':
            sad_score = sad_score + 1
        if sad_score >=5:
            break
    return sad_score

interval = 60
# Provide consolation message



while True:

    prevSong = None
    results = sp.current_user_recently_played(limit=10)
    if results["items"][9] != prevSong:
        doc_ref = db.collection("music")
        doc_ref.add({
            "title": results["items"][9]["track"]["name"],
            "sentiment": fetch_uno(),
            "date": datetime.datetime.now(datetime.timezone.utc),
        })

    prevSong = results["items"][9]

    sad_score = fetch_n_find(results) # Call your API function
    if sad_score >=5:
        sad = "The user has been playing a sad song and is possibly depressed, ONLY provide a SIMPLE caring consolation message using second person pronouns, then recommend them list of 5   happier, birghter, and motivating songs to brighten their day"
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=sad,
            max_tokens =1000,
            temperature=0.9
        )
        consolation_message = response.choices[0].text.strip()
    # Alert the user with the consolation message
        print(f"Alert: Hey, The songs you have been playing have a negative sentiment. {consolation_message}\n")
    # Pause execution for the specified interval
    time.sleep(interval)

    