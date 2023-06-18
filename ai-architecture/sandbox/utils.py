import os
import pip

try:
    import pandas as pd
    from google.cloud import firestore
    import urllib.request
except:
    pip.main(['install', 'pandas'])
    pip.main(['install', 'google-cloud-firestore'])
    import pandas as pd
    from google.cloud import firestore


def firestore_to_df(credentials: dict):
    db = firestore.Client()
    users = list(db.collection(u'users').stream())

    users_dict = list(map(lambda x: x.to_dict(), users))
    df = pd.DataFrame(users_dict)


def firebase_url_to_df(url: str):
    with urllib.request.urlopen(url) as url_file:
        df = pd.read_csv(url_file)
        return df
