import requests
import pandas as pd


def fetch_restaurant_data_from_api(api_url, headers=None):
    """
    Fetch restaurant data from an external API.

    Args:
        api_url (str): The API endpoint URL.
        headers (dict, optional): Headers for the API request, if needed, for example, for authentication.

    Returns:
        pandas dataframe: The data from the API converted to a pandas DataFrame.
    """
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return pd.json_normalize(data)
    else:
        raise Exception(f"Failed to fetch data from API. Status code: {response.status_code}")


def main():
    """
    Fetch data from api and export it to a CSV file.
    Allows fetch function to be used as a standalone script.
    """
    url = "https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json"
    data = fetch_restaurant_data_from_api(url)
    data.to_csv('../output/fetchResults.csv', index=False)


if __name__ == "__main__":
    main()
