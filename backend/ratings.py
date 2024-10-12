import requests
import os

OMDB_API_KEY = os.getenv('OMDB_API_KEY')

def get_imdb_rating(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('imdbRating', 'N/A')
    return 'N/A'

def get_rotten_tomatoes_rating(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        ratings = data.get('Ratings', [])
        for rating in ratings:
            if rating['Source'] == 'Rotten Tomatoes':
                return rating['Value']
    return 'N/A'

def get_metacritic_rating(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('Metascore', 'N/A')
    return 'N/A'

def get_all_ratings(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        imdb = data.get('imdbRating', 'N/A')
        metacritic = data.get('Metascore', 'N/A')
        rotten_tomatoes = 'N/A'
        for rating in data.get('Ratings', []):
            if rating['Source'] == 'Rotten Tomatoes':
                rotten_tomatoes = rating['Value']
                break
        return {
            'imdb': imdb,
            'rotten_tomatoes': rotten_tomatoes,
            'metacritic': metacritic
        }
    return {'imdb': 'N/A', 'rotten_tomatoes': 'N/A', 'metacritic': 'N/A'}
