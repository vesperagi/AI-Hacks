import pip
try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
    import lyricsgenius
    import openai
    import os
    import time
    import firebase_admin
    from firebase_admin import credentials, firestore
    import datetime
except:
    pip.main(["install", "spotipy"])
    pip.main(["install", "lyricsgenius"])

cred = credentials.Certificate("vigama-ai-hacks-firebase-adminsdk-5waoy-7ddd5ba925.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOT_CLIENT_ID'),
                                               client_secret=os.getenv('SPOT_CLIENT_SECRET'),
                                               redirect_uri='http://localhost:8000/callback',
                                               scope='user-read-recently-played'))

# Set up authentication for Genius API
genius_token = os.getenv('GENIUS_TOKEN')
genius = lyricsgenius.Genius(genius_token)

# Set up authentication for OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')


def fetch_uno():
    """
    Fetches the most recently played song by a Spotify user and analyzes its lyrics sentiment.
    NOTE: Requires an authenticated Spotify and Genius connection, as well as subscription to OpenAI text generation service.

    Parameters
    ----------

    No Parameters required.

    Returns
    ------
    str
        Returns the sentiment of the song lyrics as positive, negative, or neutral.
    """
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

    # return track_name = track['name']


def fetch_n_find(results):
    """
    Returns a score based on the sentiment analysis of lyrics from a list of tracks.

    The sentiment analysis is performed by OpenAI API, using only the first 10% of lyrics of a song.
    Any song that produces a 'negative' sentiment increases the sad_score by 1. The function stops if sad_score is equal to or above 5.

    Parameters
    ----------
    results : dict
        A dictionary containing the list of tracks. Each track is a dictionary containing its details such as name and artist.

    Returns
    -------
    int
        The 'sadness' score of the list of tracks, indicating how many tracks had a 'negative' sentiment.
    """
    sad_score = 0
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
        if sad_score >= 5:
            break
    return sad_score


interval = 60
# Provide consolation message

"""
This piece of code is continuously checking the Spotify API to track the most played songs of the current user. In case the last song played is different from the previous one, it adds the new song to a firestore database 'music' including its name, sentiment, and the current date.

It continues to calculate the sentiment score for the list of most recently played songs. If the sentiment score is above 5, it is inferred as the user might be depressed, and an attempt is made to generate a simple consolation message and recommends a list of 5 happier, brighter, and motivating songs to the user to brighten their day. This message is generated using OpenAI's GPT-3 'text-davinci-003' model.

The script then sleeps for a specified time interval before repeating the process.
"""
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

    sad_score = fetch_n_find(results)  # Call your API function
    if sad_score >= 5:
        sad = "The user has been playing a sad song and is possibly depressed, ONLY provide a SIMPLE caring consolation message using second person pronouns, then recommend them list of 5   happier, birghter, and motivating songs to brighten their day"
        response = openai.Completion.create(
            engine='text-davinci-003',
            prompt=sad,
            max_tokens=1000,
            temperature=0.9
        )
        consolation_message = response.choices[0].text.strip()
        # Alert the user with the consolation message
        print(f"Alert: Hey, The songs you have been playing have a negative sentiment. {consolation_message}\n")
    # Pause execution for the specified interval
    time.sleep(interval)
