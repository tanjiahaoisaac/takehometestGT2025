import os
import requests
import pandas as pd


def fetch_carpark_data_from_api(api_url, headers=None):
    """
    Fetch car park data from an external API.

    Args:
        api_url (str): The API endpoint URL for real-time car park availability.
        headers (dict, optional): Headers for the API request, if needed, for example, for authentication.

    Returns:
        dict: The car park data in JSON format.
    """
    try:
        response = requests.get(api_url, headers=headers, timeout=10)  # Set a timeout for reliability
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        return response.json()

    except requests.exceptions.Timeout:
        print("Error: The request timed out. Please try again later.")
    except requests.exceptions.ConnectionError:
        print("Error: Failed to connect to the API. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
    except ValueError:
        print("Error: Response returned is not valid JSON.")

    return {}  # Return an empty dictionary on failure


def save_data_to_csv(data, output_path):
    """
    Save the data to a CSV file.

    Args:
        data (list): Data (usually from API response) to be saved.
        output_path (str): The path where the CSV file will be saved.
    """
    try:
        if not data:
            print("Warning: No data to save. The CSV file will not be created.")
            return

        df = pd.DataFrame(data)
        df.to_csv(output_path, index=False)
        print(f"Data successfully saved to {output_path}")

    except FileNotFoundError:
        print(f"Error: Directory not found for saving the file - {output_path}")
    except PermissionError:
        print(f"Error: Permission denied when writing to {output_path}")
    except Exception as e:
        print(f"Error while saving data to CSV: {e}")


def main():
    """
    Fetch car park data from the API and export it to a CSV file.
    Allows the fetch function to be used as a standalone script.
    """
    api_url = "https://api.data.gov.sg/v1/transport/carpark-availability"

    try:
        carpark_data = fetch_carpark_data_from_api(api_url)

        if not carpark_data or not carpark_data.get("items"):
            print("Error: Fetched data is empty or malformed. No car park data available.")
            return

        output_dir = "../output"
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

        output_path = os.path.join(output_dir, "carpark_availability.csv")

        # Save the fetched data to CSV
        save_data_to_csv(carpark_data["items"], output_path)

    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
