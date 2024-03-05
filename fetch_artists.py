import pandas as pd 
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import re

# API
# To extract the Spotify artist ID from the URL 
pattern = r"/artist/([a-zA-Z0-9]+)"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="7c05329bf96e473ba85b9d6232195e02",
                                                           client_secret="2329f13c302848bd9bf497fd2d2c9f64"))
dataset = pd.read_csv('data/Spotify_Youtube.csv')

def extract_artist_id(url):
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

# Get unique values    
dataset['artist_id'] = dataset['Url_spotify'].apply(extract_artist_id)
unique_artist = dataset['artist_id'].unique()
print(unique_artist.shape)

# artist_ids = unique_artist.tolist()[:500]
artist_ids = unique_artist.tolist()

# get the artist detail in batch of 50
batch_size = 50
# num_artists_fetche = 0
fetched_artists = []
for i in range(0, len(artist_ids), batch_size):
    batch_ids = artist_ids[i:i+batch_size]
    artists = sp.artists(batch_ids)
    
    # Process the details of the artists in this batch
    for artist in artists['artists']:
        # Here you can access details of each artist in the batch
        # print("Artist:", artist['name'], "Genres:", artist['genres'])
        # num_artists_fetche += 1
        fetched_artists.append({'id': artist['id'], 'name': artist['name'],'genres': artist['genres']})
# num_artists_fetche
#fetched_artists

fetched_artists_df = pd.DataFrame(fetched_artists)
#fetched_artists_df.sample(n=10)

#save csv file
csv_filename = 'artist.csv'
fetched_artists_df.to_csv(csv_filename, index=False)
