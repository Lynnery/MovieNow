import React, { useState, FormEvent } from 'react';
import axios from 'axios';

interface MovieRequest {
  genre: string;
  max_distance: number;
  start_time: string;
  end_time: string;
  user_location: string;
}

interface BestMovie {
  title: string;
  cinema: string;
  distance: number;
  rating: number;
  price: number;
}

const App: React.FC = () => {
  const [genre, setGenre] = useState<string>('');
  const [maxDistance, setMaxDistance] = useState<number>(10);
  const [startTime, setStartTime] = useState<string>('');
  const [endTime, setEndTime] = useState<string>('');
  const [location, setLocation] = useState<string>('');
  const [bestMovie, setBestMovie] = useState<BestMovie | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const movieRequest: MovieRequest = {
        genre,
        max_distance: maxDistance,
        start_time: startTime,
        end_time: endTime,
        user_location: location
      };

      const response = await axios.post<BestMovie>('http://localhost:8000/find_best_movie', movieRequest);
      setBestMovie(response.data);
    } catch (error) {
      if (axios.isAxiosError(error)) {
        console.error('Error finding best movie:', error.response?.status, error.response?.data);
        alert(`Error: ${error.response?.data?.detail || 'An unknown error occurred'}`);
      } else {
        console.error('Error finding best movie:', error);
        alert('An unknown error occurred');
      }
    }
  };

  return (
    <div className="App">
      <h1>Find the Best Movie</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="genre">Genre:</label>
          <input
            type="text"
            id="genre"
            value={genre}
            onChange={(e) => setGenre(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="maxDistance">Max Distance (km):</label>
          <input
            type="range"
            id="maxDistance"
            min="1"
            max="50"
            value={maxDistance}
            onChange={(e) => setMaxDistance(Number(e.target.value))}
          />
          <span>{maxDistance} km</span>
        </div>
        <div>
          <label htmlFor="startTime">Start Time:</label>
          <input
            type="time"
            id="startTime"
            value={startTime}
            onChange={(e) => setStartTime(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="endTime">End Time:</label>
          <input
            type="time"
            id="endTime"
            value={endTime}
            onChange={(e) => setEndTime(e.target.value)}
            required
          />
        </div>
        <div>
          <label htmlFor="location">Location:</label>
          <input
            type="text"
            id="location"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            required
          />
        </div>
        <button type="submit">Find Best Movie</button>
      </form>
      {bestMovie && (
        <div>
          <h2>Best Movie:</h2>
          <p>Title: {bestMovie.title}</p>
          <p>Cinema: {bestMovie.cinema}</p>
          <p>Distance: {bestMovie.distance} km</p>
          <p>Rating: {bestMovie.rating}</p>
          <p>Price: ${bestMovie.price}</p>
        </div>
      )}
    </div>
  );
};

export default App;
