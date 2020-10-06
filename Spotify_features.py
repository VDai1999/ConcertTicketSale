# Import packages
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials #To access authorised Spotify data
import csv
import pandas as pd

# ID retrieved from personal spotify account
client_id = "2039381fcda54f7690fdbb96819319f7"
client_secret = "9355c0e4535a4b709ef77dccb6aa7781"

# Access to API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# A function to get song feature in python
def song_features(result):
    songFeature = {}
    track = result['tracks']['items'][0]['uri']
    features = sp.audio_features(track)
    cols = ['danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 
            'liveness', 'valence', 'tempo', 'type', 'duration_ms']
    
    songFeature['artist'] = result['tracks']['items'][0]['artists'][0]['name']
    songFeature['song'] = result['tracks']['items'][0]['name']
    
    for col in cols:
        songFeature[col] = features[0][col]
        
    pop = sp.track(track)
    songFeature['popularity'] = pop['popularity']
    
    return songFeature

# Read in the csv file that contain the name of the song
df = pd.read_csv('YoutubeStat_Dai.csv')
df.head()
# Strip out unnecessary symbols
df['Song'] = df.Song.str.replace(r"\(.*\)","").str.replace(r"\[.*\]","")


def main():
    stop = False
    listSongFeature = []
    
    # Get statistics
    for i in range (len(df)):
        artist = df['Artist'][i]
        song = df['Song'][i].rstrip()
        result = sp.search(q=artist+ " " + song, limit=1)
        sf = song_features(result) 
        listSongFeature.append(sf)
    
    # Columns that will be written in a csv file
    csv_columns = ['artist', 'song', 'danceability', 'energy', 'speechiness', 'acousticness', 'instrumentalness', 
                   'liveness', 'valence', 'tempo', 'type', 'duration_ms', 'popularity']
    csv_file = "features.csv"
    
    # Write the statistics into a csv file
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(csv_columns)
            
            for lsf in listSongFeature:
                temp = list()
                for key in lsf.keys():
                    temp.append(lsf[key])
                writer.writerow(temp)
            
    except IOError:
        print("I/O error")
     
