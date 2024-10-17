# app.py
from flask import Flask, jsonify
from flask_cors import CORS
from src.module1 import refresh_main,API
import logging
import warnings

warnings.filterwarnings("ignore")

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    # Set up logging
    logging.basicConfig(level=logging.INFO)

    @app.route('/<input_parameter>', methods=['GET'])
    def get_data(input_parameter):
        """Endpoint to get data based on the input parameter."""
        try:
            if input_parameter == 'refresh':
            # Call refresh_main if input_parameter is 'refresh'
                print("Data is refreshing")
                result = refresh_main()
                return  "Data Refreshed! "
                
            else:
            # Call your API function (assuming it's named fetch_data or similar)
                result = API(input_parameter)

            if result.empty:
                return jsonify({"error": "No data returned. Please check the URL."}), 404
            return jsonify(result.to_dict(orient='records')), 200
        except Exception as e:
            logging.error(f"Error fetching Data: {e}")  # Log the error
            return jsonify({"error": str(e)}), 500
    
    @app.route('/', methods=['GET'])
    def root():
        return "Welcome! Please provide a url parameter from 'countries', 'GDP', 'exports'. 'Refresh' or 'population'."

    return app







