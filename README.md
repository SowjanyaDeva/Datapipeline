# World Bank Data API and ETL Pipeline using Flask and DuckDB

## Overview
This project creates a simple Flask-based web application that fetches data from the World Bank API, processes it, and stores it in DuckDB. The application provides API endpoints for refreshing the data and retrieving key economic metrics such as GDP, population, and exports.

## Features
1. **API Endpoints**:  
   - `/refresh`: Refreshes the data from the World Bank API and loads it into DuckDB.
   - `/[metric]`: Returns data for a specific metric, such as `countries`, `GDP`, `exports`, or `population`.
   - `/`: Root endpoint with welcome message.

2. **Data Processing**:  
   - Fetches **country codes** and **economic indicators** from the World Bank API.
   - Stores **GDP**, **population**, and **export data** in DuckDB.
   - Supports data transformation and reporting with DuckDB queries.

3. **Database**: 
   - Uses DuckDB as the storage layer to efficiently handle analytical queries.

## Prerequisites
- Python 3.x
- DuckDB
- Flask
- Pandas
- Requests
- Flask-CORS

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SowjanyaDeva/Datapipeline.git
   cd Datapipeline
