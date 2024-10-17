import pandas as pd
import requests
import duckdb
import warnings
warnings.filterwarnings("ignore")

# Base URL used in all the API calls
BASE_URL = 'https://api.worldbank.org/v2/'
params = dict()
params['format'] = 'json'  # Ensure we receive a JSON response
params['per_page'] = '100'  # Change the default page size to 100 to avoid multiple API calls

# Indicator codes for fetching data
INDICATOR_CODES = ['SP.POP.TOTL', 'NY.GDP.MKTP.CD', 'TX.VAL.MRCH.CD.WT']

# Fetch country codes and names dynamicallypip
def get_country_codes():
    country_url = "https://api.worldbank.org/v2/country?format=json&per_page=300"
    try:
        country_response = requests.get(country_url)
        country_response.raise_for_status()  # Raise an error if the response status is not 200
        country_data = country_response.json()
        # Initialize an empty dictionary to store country codes and names
        result_dict = {}
        for country in country_data[1]:  # Assuming data[1] contains the relevant list of items
            result_dict[country['id']] = country['name']
        return result_dict                                                                                                                                          
    except requests.exceptions.RequestException as e:
        print(f"Error fetching country data: {e}")
        return {}  # Return an empty dictionary if the request fails
    except (ValueError, KeyError, IndexError) as e:


        print(f"Error processing country data: {e}")
        return {}

# Function to fetch and process data from World Bank API
def loadJSONData(country_code):
    data_list = []  # Initialize an empty list to store data

    for indicator in INDICATOR_CODES:
        url = BASE_URL + 'countries/' + country_code.lower() + '/indicators/' + indicator
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Check for HTTP errors
            data_entries = response.json()[1] if len(response.json()) > 1 else None

            if data_entries is None:
                continue  # Skip if no data

            for entry in data_entries:
                country_code = entry.get('country', {}).get('id', None)
                country_name = entry.get('country', {}).get('value', 'None')
                indicator_id = entry.get('indicator', {}).get('id', None)
                indicator_value = entry.get('indicator', {}).get('value', None)
                value = entry.get('value', None)
                date = entry.get('date', None)

                # Create a new dictionary for each indicator and append it to data_list
                data_list.append({
                    'Country Code': country_code,
                    'Country Name': country_name,
                    'Indicator ID': indicator_id,
                    'Indicator Value': indicator_value,
                    'Value': value,
                    'Date': date
                })
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {country_code}: {e}")
        except (ValueError, KeyError, IndexError) as e:
            print(f"Error processing data for {country_code}: {e}")
    
    return data_list

# Main function to execute the data processing and loading into DuckDB
def refresh_main(input_parameter = None):
    try:
        # Fetch country codes
        result_dict = get_country_codes()
        if not result_dict:
            print("No country data available. Exiting.")
            return

        # Initialize an empty DataFrame to store all data
        all_data_df = pd.DataFrame(columns=["Country Code", "Country Name", "Indicator ID", "Indicator Value", "Value", "Date"])

        # Fetch data for each country and append it to the DataFrame
        for country_code in result_dict:
            country_data = loadJSONData(country_code)
            if country_data:
                all_data_df = pd.concat([all_data_df, pd.DataFrame(country_data).fillna(0)], ignore_index=True)

        # Pivot the DataFrame to have Indicator Values as columns
        pivot_df = all_data_df.pivot_table(index=['Country Code', 'Country Name'],
                                           columns='Indicator Value',
                                           values='Value').reset_index()

        
        pivot_df.columns.name = None  # Remove the column grouping name

        # Convert specific columns to integer after handling NaN values
        pivot_df[['GDP (current US$)', 'Merchandise exports (current US$)', 'Population, total']] = pivot_df[['GDP (current US$)', 'Merchandise exports (current US$)', 'Population, total']].fillna(0).astype(int)

        # Print the processed DataFrame
        print("Processed DataFrame:")
        print(pivot_df.head())

        countries_df = pivot_df[["Country Code", "Country Name"]]
        GDP_df = pivot_df[["Country Code", "Country Name", "GDP (current US$)"]]
        exports_df = pivot_df[["Country Code", "Country Name", "Merchandise exports (current US$)"]]
        population_df = pivot_df[["Country Code", "Country Name", "Population, total"]]

        dataframes = {
                'countries': countries_df,
                'GDP': GDP_df,
                'exports': exports_df,
                'population': population_df
            }


    
        # Connect to DuckDB (persistent)
        try:
            con = duckdb.connect(database='worldbank_data.duckdb') 
            for i in ["countries", "GDP", "exports", "population"]:
                con.execute("CREATE TABLE IF NOT EXISTS country_economic_metrics_{} AS SELECT * FROM {}_df".format(i, i))
            # Verify the data is loaded into DuckDB
                query_result = con.execute("SELECT * FROM country_economic_metrics_{} LIMIT 5".format(i)).fetchdf()
                print("Data loaded into DuckDB country_economic_metrics_{} table:".format(i))
                print(query_result)
        except Exception as e:
            print(f"Error loading data into DuckDB: {e}")

        return print("Data Refreshed! ")
    

    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def API(input_parameter):
    con = duckdb.connect(database='worldbank_data.duckdb') 
    result = con.execute("SELECT * FROM country_economic_metrics_{}".format(input_parameter)).df()
    return result
   


# Run the main function
if __name__ == "__main__":
    refresh_main()
