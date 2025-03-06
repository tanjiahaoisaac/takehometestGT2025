import requests
import pandas as pd
import os


def fetch_restaurant_data_from_api(api_url, headers=None):
    """
    Fetch restaurant data from an external API.

    Args:
        api_url (str): The API endpoint URL.
        headers (dict, optional): Headers for the API request, if needed, for example, for authentication.

    Returns:
        json: The data from the API in json format.
    """
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Will raise HTTPError for bad responses (4xx and 5xx)
        
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error during API request: {e}")
    except ValueError:
        raise Exception("Error: Response returned is not a valid JSON.")
    

def save_data_to_csv(df, output_path):
    """
    Save the dataframe to a CSV file.

    Args:
        df (pandas dataframe): The dataframe to save.
        output_path (str): The path where the CSV file should be saved.

    Returns:
        None
    """
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Data successfully saved to {output_path}")
    except Exception as e:
        raise Exception(f"Failed to save data to CSV: {e}")


def main():
    """
    Fetch data from the API and export it to a CSV file.
    Allows the fetch function to be used as a standalone script.
    """
    url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
    
    try:
        # Fetch data from the API
        data = fetch_restaurant_data_from_api(url)
        
        # Convert the dictionary to a pandas DataFrame
        df = pd.DataFrame(data)
        
        # Check if the dataframe is empty
        if df.empty:
            raise ValueError("Fetched data is empty. No data to save.")
        
        # Save the data to a CSV file
        output_path = '../output/fetchResults.csv'
        save_data_to_csv(df, output_path)
    
    except (requests.exceptions.RequestException, ValueError, Exception) as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
