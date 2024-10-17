##World Bank Data API and ETL Pipeline using Flask and DuckDB
Overview
This project creates a simple Flask-based web application that fetches data from the World Bank API, processes it, and stores it in DuckDB. The application provides API endpoints for refreshing the data and retrieving key economic metrics such as GDP, population, and exports.

Features
API Endpoints:

/refresh: Refreshes the data from the World Bank API and loads it into DuckDB.
/[metric]: Returns data for a specific metric, such as countries, GDP, exports, or population.
/: Root endpoint with welcome message.
Data Processing:

Fetches country codes and economic indicators from the World Bank API.
Stores GDP, population, and export data in DuckDB.
Supports data transformation and reporting with DuckDB queries.
Database:

Uses DuckDB as the storage layer to efficiently handle analytical queries.
Prerequisites
Python 3.x
DuckDB
Flask
Pandas
Requests
Flask-CORS
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/SowjanyaDeva/Datapipeline.git
cd Datapipeline
Install Dependencies: Use pip to install the required Python packages:

bash
Copy code
pip install flask flask-cors pandas requests duckdb
Run the Application:

bash
Copy code
python app.py
Usage
Endpoints
/refresh:

Refreshes data from the World Bank API and stores it in DuckDB.
Example:
bash
Copy code
GET http://localhost:5000/refresh
/countries, /GDP, /exports, /population:

Returns data for a specific metric.
Example:
arduino
Copy code
GET http://localhost:5000/GDP
/ (Root):

Displays a welcome message with instructions.
Example Output:
Top 10 GDP per capita query:
bash
Copy code
SELECT gdp."Country Name", 
       gdp."GDP (current US$)" / pop."Population, total" AS gdp_per_capita
FROM country_economic_metrics_GDP AS gdp
JOIN country_economic_metrics_population AS pop
ON gdp."Country Name" = pop."Country Name"
ORDER BY gdp_per_capita DESC
LIMIT 10;
Project Structure
bash
Copy code
Datapipeline/
│
├── app.py              # Flask application
├── src/
│   └── module1.py      # Contains refresh and API functions
├── worldbank_data.duckdb  # DuckDB database file
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation (this file)
Flask API Overview
create_app(): Initializes the Flask app and enables CORS.
Logging: Uses the logging library for error tracking.
Routes:
/refresh fetches data from the World Bank API and stores it in DuckDB.
<input_parameter> routes retrieve data from the corresponding tables in DuckDB.
Database Schema
Four tables are created in DuckDB:

country_economic_metrics_countries
country_economic_metrics_GDP
country_economic_metrics_exports
country_economic_metrics_population
Error Handling
API Errors:
Returns 404 if no data is available.
Logs errors using Python’s logging module and provides 500 errors for unexpected issues.
Future Enhancements
Add authentication to the API.
Implement pagination for large datasets.
Cache API responses to reduce load time.
Automate regular data refresh using CRON or similar schedulers.
Contributing
If you’d like to contribute:

Fork the repository.
Create a feature branch (git checkout -b feature-branch).
Commit your changes (git commit -m 'Add some feature').
Push to the branch (git push origin feature-branch).
Open a pull request.
License
This project is licensed under the MIT License.
