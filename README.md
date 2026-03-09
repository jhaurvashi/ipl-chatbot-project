# IPL Analytics Chatbot (Flask)

Simple IPL analytics chatbot-style web app built with Flask.  
It exposes APIs for:

- Top scorer across the dataset
- IPL winner (most wins) by year

and provides a small HTML UI that calls these APIs.

## Project structure

- `app.py` – Flask application entrypoint (WSGI `app` object for production)
- `ipl_service.py` – IPL analytics service that loads and queries the CSV data
- `data/ipl_matches.csv` – Sample IPL matches dataset (replace with your own)
- `templates/index.html` – Frontend UI (served at `/`)
- `static/styles.css` – Styling for the UI
- `requirements.txt` – Python dependencies
- `Procfile` – Process type for IBM Cloud (Gunicorn)
- `runtime.txt` – Python runtime version hint

## CSV dataset format

The backend expects a CSV file at `data/ipl_matches.csv` with at least these columns:

- `season` – season year (e.g. `2016`)
- `match_id` – unique match identifier
- `team1` – first team
- `team2` – second team
- `winner` – winning team name
- `top_scorer` – player who scored the most runs in that match
- `top_scorer_runs` – integer runs scored by `top_scorer` in that match

You can replace `data/ipl_matches.csv` with a fuller IPL dataset as long as it has
the columns above.

## API endpoints

### `GET /api/top-scorer`

**Description**: Returns the player with the highest total runs across all matches
(summing `top_scorer_runs` per `top_scorer`).

**Example response**:

```json
{
  "player": "AB de Villiers",
  "total_runs": 450
}
```

### `GET /api/winner-by-year?year=2016`

**Description**: Returns the team with the most wins for the given season year.

Query parameters:

- `year` (required, integer) – season year

**Example response**:

```json
{
  "year": 2016,
  "team": "Sunrisers Hyderabad",
  "wins": 11
}
```

## Running locally

1. Create and activate a virtual environment (recommended).

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # on Windows
   # source .venv/bin/activate  # on macOS/Linux
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the Flask app:

   ```bash
   python app.py
   ```

4. Open the browser at `http://localhost:5000`.

## IBM Cloud deployment (Cloud Foundry)

1. Ensure you have the IBM Cloud CLI and Cloud Foundry plugin installed and logged in.

2. From the project root (where `Procfile`, `requirements.txt`, and `runtime.txt` live), run:

   ```bash
   ibmcloud cf push ipl-analytics-chatbot
   ```

   This will:

   - Install dependencies from `requirements.txt`
   - Use `runtime.txt` to select the Python version
   - Start the app with `gunicorn app:app` as defined in `Procfile`

3. After deployment, IBM Cloud will output the public URL for your app.

