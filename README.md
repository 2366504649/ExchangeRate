# Exchange Rate Tracker

A Python-based application to track daily exchange rates for USD, JPY, THB, MYR, SGD, and PHP against CNY. It scrapes data from the Bank of China, stores it in a SQLite database, and provides a web dashboard for visualization.

## Features

- **Data Crawling**: Scrapes real-time exchange rates from Bank of China.
- **Data Storage**: Persists data in a local SQLite database.
- **Web Dashboard**: Visualizes historical trends with interactive charts.
- **Daily Summary**: Provides daily exchange rate changes and simple trading suggestions.
- **Scheduler**: Automates daily data fetching.

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Create and activate a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### 1. Initialize and Fetch Data
Before starting the web app, it's good to fetch the latest data. This will also create the database if it doesn't exist.
```bash
python fetcher.py
```

### 2. Run the Web Application
Start the Flask development server:
```bash
python app.py
```
Access the dashboard at: [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 3. Run the Scheduler (Optional)
To automatically fetch data every day at 09:00 AM:
```bash
python scheduler.py
```

## API Documentation

### 1. Get Historical Data
Returns historical exchange rates for a specific currency.

- **Endpoint**: `/api/history`
- **Method**: `GET`
- **Parameters**:
    - `currency` (optional): Currency code (default: `USD`). Options: `USD`, `JPY`, `THB`, `MYR`, `SGD`, `PHP`.
- **Response**: JSON array of objects.
  ```json
  [
    {
      "date": "2023-10-27",
      "rate": 731.5
    },
    ...
  ]
  ```

### 2. Get Daily Summary
Returns a summary of the latest exchange rate changes and suggestions.

- **Endpoint**: `/api/summary`
- **Method**: `GET`
- **Parameters**: None
- **Response**: JSON array of objects.
  ```json
  [
    {
      "currency": "USD",
      "current": 731.5,
      "change": 0.05,
      "percent": 0.01,
      "trend": "up",
      "suggestion": "Stable."
    },
    ...
  ]
  ```

## Project Structure

- `app.py`: Main Flask application.
- `database.py`: Database models and configuration.
- `fetcher.py`: Script to scrape data from Bank of China.
- `scheduler.py`: Script to run the fetcher periodically.
- `templates/index.html`: Frontend HTML dashboard.
- `static/`: CSS and JavaScript files.
