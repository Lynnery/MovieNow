
## Setup and Running the Application

### Backend

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Set up your `.env` file with your OMDB API key:
   ```
   OMDB_API_KEY=your_api_key_here
   ```

6. Run the backend server:
   ```
   python backend.py
   ```

   The server will start running on `http://localhost:8000`.

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install the required npm packages:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`.

## API Endpoints

- `POST /find_best_movie`: Finds the best movie based on user preferences and location.

## Technologies Used

- Backend: FastAPI, Python
- Frontend: React, TypeScript, Vite
- API: OMDB API for movie ratings

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- OMDB API for providing movie data
- OpenAI's ChatGPT for development assistance