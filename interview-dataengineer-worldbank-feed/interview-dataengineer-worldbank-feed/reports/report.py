import duckdb
import pandas as pd

# Database connection 
con = duckdb.connect(database='worldbank_data.duckdb') 

def top_10_gdp_per_capita(con):
    """
    Function to get the top 10 countries by GDP per capita.
    
    Args:
        con: DuckDB connection object.
        
    Returns:
        pd.DataFrame: Top 10 countries by GDP per capita.
    """
    query = """
    SELECT gdp."Country Name", 
           gdp."GDP (current US$)" / pop."Population, total" AS gdp_per_capita
    FROM country_economic_metrics_GDP AS gdp
    JOIN country_economic_metrics_population AS pop
    ON gdp."Country Name" = pop."Country Name"
    ORDER BY gdp_per_capita DESC
    LIMIT 10

    """
    result = con.execute(query).df()
    return result

def total_gdp_per_country(con):
    """
    Function to get the total GDP per country.
    
    Args:
        con: DuckDB connection object.
        
    Returns:
        pd.DataFrame: Total GDP per country.
    """
    query = """
    SELECT "Country Name", 
           SUM("GDP (current US$)") AS total_gdp
    FROM country_economic_metrics_GDP
    GROUP BY "Country Name"
    """
    result = con.execute(query).df()
    return result

def report_main(input_parameter= None):
    """
    Main function to refresh data and generate reports.
    """
    # Get Top 10 Countries by GDP per Capita
    top_10 = top_10_gdp_per_capita(con)
    print("Top 10 Countries by GDP per Capita:")
    print(top_10.to_string(index=False))

    # Get Total GDP per Country
    total_gdp = total_gdp_per_country(con)
    print("\nTotal GDP per Country:")
    print(total_gdp.to_string(index=False))

if __name__ == "__main__":
    report_main()  # Call the main function to execute the refresh and report generation
