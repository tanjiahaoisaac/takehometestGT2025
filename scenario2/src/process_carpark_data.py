import pandas as pd
from datetime import datetime, timedelta


def parse_fetched_data(api_response):
    """
    Process car park data from the API response into a DataFrame.

    Args:
        api_response (dict): The API response in JSON format containing car park data.

    Returns:
        pandas dataframe: A DataFrame containing the car park information.
    """
    carpark_rows = []

    for item in api_response.get("items", []):  
        for carpark in item.get("carpark_data", []):
            if "carpark_info" not in carpark or not carpark["carpark_info"]:
                print(f"Warning: Missing 'carpark_info' for car park {carpark.get('carpark_number', 'Unknown')}.")
                continue

            carpark_info = carpark["carpark_info"][0]  # Extract first entry

            carpark_row = {
                "carpark_number": carpark.get("carpark_number", "Unknown"),
                "total_lots": int(carpark_info.get("total_lots", 0)),
                "lots_available": int(carpark_info.get("lots_available", 0)),
                "lot_type": carpark_info.get("lot_type", "N/A"),
                "update_datetime": carpark.get("update_datetime", None),
            }

            carpark_rows.append(carpark_row)

    return pd.DataFrame(carpark_rows)


def load_hdb_carpark_info(file_path: str):
    """
    Load the HDB carpark information from a CSV file into a DataFrame.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas dataframe: DataFrame containing the HDB carpark information.
    """
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except pd.errors.EmptyDataError:
        print(f"Error: CSV file is empty - {file_path}")
    except Exception as e:
        print(f"Error loading CSV file: {e}")

    return pd.DataFrame()


def clean_carpark_data(df: pd.DataFrame, hdb_file_path: str):
    """
    Clean the car park data by merging with HDB information and applying necessary filters.

    Args:
        df (dataframe): The car park data from the API response.
        hdb_file_path (str): Path to the HDB carpark CSV file.

    Returns:
        pd.DataFrame: A cleaned DataFrame containing merged and filtered car park data.
    """
    try:
        hdb_carpark_info = load_hdb_carpark_info(hdb_file_path)

        if hdb_carpark_info.empty:
            print("Warning: HDB car park CSV data is empty or failed to load.")
            return df  # Return original API data as fallback

        # Perform a left join on car park numbers
        merged_df = pd.merge(df, hdb_carpark_info, how="left", left_on="carpark_number", right_on="car_park_no")

        # Drop rows with missing values
        merged_df = merged_df.dropna()

        # Filter out rows with negative total_lots or lots_available
        merged_df = merged_df[(merged_df["total_lots"] >= 0) & (merged_df["lots_available"] >= 0)]

        # Convert 'update_datetime' to datetime format
        merged_df["update_datetime"] = pd.to_datetime(merged_df["update_datetime"], errors="coerce")

        # Filter out rows where 'update_datetime' is in the future or more than 15 minutes old
        current_time = datetime.now()
        fifteen_mins_ago = current_time - timedelta(minutes=15)

        cleaned_df = merged_df[(merged_df["update_datetime"] <= current_time) & 
                               (merged_df["update_datetime"] >= fifteen_mins_ago)]

        # Drop unnecessary columns
        cleaned_df = cleaned_df.drop(columns=["car_park_no"], errors="ignore")

        return cleaned_df

    except Exception as e:
        print(f"Error cleaning car park data: {e}")
        return df  # Return original API data as fallback


def process_carpark_data(api_response, hdb_file_path: str):
    """
    Final function to process and clean the car park data by calling necessary functions.

    Args:
        api_response (dict): The API response in JSON format containing car park data.
        hdb_file_path (str): Path to the HDB carpark CSV file.

    Returns:
        pandas dataframe: A fully cleaned DataFrame containing car park information.
    """
    try:
        df = parse_fetched_data(api_response)
        if df.empty:
            print("Warning: Parsed car park data is empty.")
            return df

        cleaned_df = clean_carpark_data(df, hdb_file_path)
        return cleaned_df

    except Exception as e:
        print(f"Unexpected error in processing car park data: {e}")
        return pd.DataFrame()
