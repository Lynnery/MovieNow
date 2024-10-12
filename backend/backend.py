from dotenv import load_dotenv
load_dotenv()  # This line should be at the top of the file

import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from bs4 import BeautifulSoup
import requests
import os
from ratings import get_imdb_rating, get_rotten_tomatoes_rating, get_metacritic_rating, get_all_ratings
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class MovieRequest(BaseModel):  
    genre: str
    max_distance: float
    start_time: str
    end_time: str
    user_location: str  # Make sure this is str, not dict


@app.post("/find_best_movie")
async def find_best_movie(request: MovieRequest):
    # 1. Find nearby cinemas using Google Maps API
    print(request)
    cinemas = find_nearby_cinemas(request.user_location, request.max_distance)
    
    if not cinemas:
        raise HTTPException(status_code=404, detail="No cinemas found within the specified distance")
    
    # 2. Scrape movie information from cinema websites
    movies = scrape_movie_info(cinemas)
    
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found in the nearby cinemas")
    
    # 3. Filter movies by genre and time
    filtered_movies = filter_movies(movies, request.genre, request.start_time, request.end_time)
    
    if not filtered_movies:
        raise HTTPException(status_code=404, detail="No movies match the specified genre and time range")
    
    # 4. Get movie ratings from IMDb, Rotten Tomatoes, and Metacritic
    rated_movies = get_movie_ratings(filtered_movies)
    
    if not rated_movies:
        raise HTTPException(status_code=404, detail="Unable to retrieve ratings for the filtered movies")
    
    # 5. Calculate overall score and sort movies
    best_movie = find_best_movie_by_score(rated_movies)
    
    return best_movie


def find_nearby_cinemas(location: str, max_distance: float):
    # Construct the Google search URL
    search_url = f"https://www.google.com/search?q=cinemas+near+{location}"
    
    # Send a request to Google
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(search_url, headers=headers)
    
    # Parse the response content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract cinema information
    cinemas = []
    for result in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        name = result.get_text()
        address = result.find_next('div', class_='BNeawe UPmit AP7Wnd').get_text()
        cinemas.append({
            'name': name,
            'address': address,
            'location': None  # Location data might not be available
        })
    
    return cinemas


def scrape_movie_info(cinemas):
    # Use BeautifulSoup to scrape movie information from cinema websites
    movies = []
    for cinema in cinemas:
        # This is a placeholder implementation. In a real-world scenario,
        # you would need to scrape actual cinema websites.
        response = requests.get(f"https://example-cinema-website.com/{cinema['name']}")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract movie information (this is just an example)
        movie_elements = soup.find_all('div', class_='movie')
        for movie_element in movie_elements:
            movies.append({
                'title': movie_element.find('h2').text,
                'showtime': movie_element.find('span', class_='showtime').text,
                'cinema': cinema['name']
            })
    
    return movies


def filter_movies(movies, genre, start_time, end_time):
    # Filter movies based on genre and time range
    filtered_movies = []
    for movie in movies:
        movie_time = datetime.datetime.strptime(movie['showtime'], '%H:%M').time()
        start = datetime.datetime.strptime(start_time, '%H:%M').time()
        end = datetime.datetime.strptime(end_time, '%H:%M').time()
        
        if start <= movie_time <= end:
            # Here we assume the genre is part of the movie information
            # In a real implementation, you might need to fetch this separately
            if genre.lower() in movie['title'].lower():
                filtered_movies.append(movie)
    
    return filtered_movies


def get_movie_ratings(movies):
    # Scrape ratings from IMDb, Rotten Tomatoes, and Metacritic
    rated_movies = []
    for movie in movies:
        imdb_rating = get_imdb_rating(movie['title'])
        rotten_tomatoes_rating = get_rotten_tomatoes_rating(movie['title'])
        metacritic_rating = get_metacritic_rating(movie['title'])
        
        rated_movies.append({
            **movie,
            'ratings': {
                'imdb': imdb_rating,
                'rotten_tomatoes': rotten_tomatoes_rating,
                'metacritic': metacritic_rating
            }
        })
    
    return rated_movies


def find_best_movie_by_score(rated_movies):
    if not rated_movies:
        raise HTTPException(status_code=404, detail="No movies available to rank")
    
    best_movie = max(rated_movies, key=lambda m: (
        m['ratings']['imdb'] * 10 +
        m['ratings']['rotten_tomatoes'] +
        m['ratings']['metacritic']
    ) / 3)
    
    return best_movie


def test_ratings():
    movies = ["The Shawshank Redemption", "The Godfather", "Pulp Fiction"]
    
    for movie in movies:
        print(f"Getting ratings for: {movie}")
        ratings = get_all_ratings(movie)
        print(f"IMDb: {ratings['imdb']}")
        print(f"Rotten Tomatoes: {ratings['rotten_tomatoes']}")
        print(f"Metacritic: {ratings['metacritic']}")
        print("---")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

    # Comment out or remove the test_ratings() call if you don't want it to run on every reload
    # test_ratings()
