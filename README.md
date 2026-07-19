# 🌏 Japan Earthquake Analysis

A data pipeline that collects, cleans, combines, and analyzes earthquake data in Japan from multiple sources (USGS, GEOFON, EMSC, and a messy manual dataset), then loads it into a MySQL database for querying and visualization.

## 📁 Project Structure

```
.
├── main.py                      # Pipeline entry point
├── requirements.txt
├── conftest.py
│
├── data/
│   ├── raw/                     # Raw CSVs from each source
│   └── processed/               # Cleaned & combined dataset (All_csv.csv)
│
├── src/
│   ├── ingestors/               # Data collection from each source (USGS, GEOFON, EMSC)
│   ├── processing/               # Cleaning, merging, geometry calculations
│   ├── database/                 # DB connection & SQL queries
│   ├── visualization/            # Charts and plots
│   └── analysis/                 # Summary tables & conclusions
│
├── tests/                        # Unit tests for each module
└── docs/                         # Additional documentation
```

## ⚙️ Requirements

- Python 3.10+
- MySQL server (for the database step)

Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

Run the full pipeline from the project root:
```bash
python main.py
```

This will:
1. Check and install missing dependencies
2. Clean and combine the four raw datasets (`src/processing/all_csv.py`)
3. Generate visualizations (`src/visualization/visualization.py`)
4. Optionally insert data into MySQL and run analytical queries (`src/database/`)

## 🗄️ Database Configuration

Before running the database step, create a `.env` file in the project root with your MySQL credentials:
```
DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=earthquakes_db
```
`src/database/database.py` reads these values to build the SQLAlchemy engine.

## 🧪 Running Tests

From the project root:
```bash
python -m pytest tests/
```

## 📊 Data Sources

| Source | Description |
|---|---|
| USGS | United States Geological Survey earthquake catalog |
| GEOFON | GFZ German Research Centre for Geosciences |
| EMSC | European-Mediterranean Seismological Centre |
| Messy Dataset | Manually collected data with inconsistent formatting, used to demonstrate data-cleaning techniques |

## 📈 Key Analyses

- Earthquake counts and averages grouped by month and severity category
- Mean/max magnitude and depth by region
- Regional distribution of earthquake frequency
- Geometric distance calculations relative to reference points

## 👥 Contributors

Built as a group project during the Quera Bootcamp.

## 📄 License

This project is for educational purposes as part of the Quera Bootcamp.
