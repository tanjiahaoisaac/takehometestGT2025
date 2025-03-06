import time
import requests
import pandas as pd
from src.fetch_carpark_data import fetch_carpark_data_from_api
from src.process_carpark_data import process_carpark_data


def search_carpark(df, carpark_number):
    """
    Search for a specific car park number in the DataFrame.

    Args:
        df (pd.DataFrame): The cleaned DataFrame containing car park data.
        carpark_number (str): The car park number to search for.

    Returns:
        pd.DataFrame: A DataFrame with the search results.
    """
    try:
        if "carpark_number" not in df.columns:
            print("Error: 'carpark_number' column not found in data.")
            return pd.DataFrame()

        return df[df["carpark_number"].str.upper() == carpark_number.upper()]
    
    except Exception as e:
        print(f"Unexpected error during search: {e}")
        return pd.DataFrame()


def display_search_results(search_results):
    """
    Display search results in a structured format.

    Args:
        search_results (pd.DataFrame): The DataFrame containing the search results.
    """
    if search_results.empty:
        print("\nNo results found.\n")
        return

    for _, row in search_results.iterrows():
        print("\n" + "=" * 50)
        print(f"🔹 Car Park Number: {row['carpark_number']}")
        print("=" * 50)

        # Address and Location Details
        print("\n📍 Address and Location Details")
        print(f"   ➤ Address: {row.get('address', 'N/A')}")

        # Parking System Information
        print("\n🅿️ Parking System Information")
        print(f"   ➤ Parking System Type: {row.get('type_of_parking_system', 'N/A')}")

        # Capacity and Availability
        print("\n🚗 Capacity and Availability")
        print(f"   ➤ Total Lots: {row.get('total_lots', 'N/A')}")
        print(f"   ➤ Available Lots: {row.get('lots_available', 'N/A')}")
        print(f"   ➤ Lot Type: {row.get('lot_type', 'N/A')}")

        # Operating Hours and Rules
        print("\n⏰ Operating Hours and Rules")
        print(f"   ➤ Short-Term Parking: {row.get('short_term_parking', 'N/A')}")
        print(f"   ➤ Free Parking: {row.get('free_parking', 'N/A')}")
        print(f"   ➤ Night Parking: {row.get('night_parking', 'N/A')}")
        print(f"   ➤ Number of Decks: {row.get('car_park_decks', 'N/A')}")
        print(f"   ➤ Gantry Height Limit: {row.get('gantry_height', 'N/A')}m")
        print(f"   ➤ Basement Parking: {row.get('car_park_basement', 'N/A')}")

        # Coordinates
        print("\n📌 Coordinates")
        print(f"   ➤ X Coordinate: {row.get('x_coord', 'N/A')}")
        print(f"   ➤ Y Coordinate: {row.get('y_coord', 'N/A')}")

        # Last Update Time
        print("\n📅 Last Update")
        print(f"   ➤ Updated On: {row.get('update_datetime', 'N/A')}")
        print("=" * 50 + "\n")


def main_loop():
    final_df = None
    api_url = "https://api.data.gov.sg/v1/transport/carpark-availability"
    csv_file_path = "data/HDBCarparkInformation.csv"

    while True:
        try:
            if final_df is None:
                print("\nFetching car park data...")
                fetched_data = fetch_carpark_data_from_api(api_url)
                
                # Check if fetched data is empty, indicating an issue
                if not fetched_data or fetched_data == {}:
                    print("Error: No data fetched from the API.")
                    
                    # Prompt user to either retry or exit
                    user_input = input("Press 'R' to retry fetching the data or 'exit' to quit: ").strip()
                    if user_input.lower() == 'exit':
                        print("\nExiting the program.")
                        break
                    elif user_input.lower() == 'r':
                        continue  # Retry fetching data
                    else:
                        print("Invalid input. Please enter 'R' to retry or 'exit' to quit.")
                        continue

                try:
                    print("\nProcessing car park data...")
                    final_df = process_carpark_data(fetched_data, csv_file_path)
                except Exception as e:
                    print(f"Error processing data: {e}")
                    continue

            user_input = input("\nEnter a car park number, 'R' to refresh, or 'exit' to quit: ").strip()

            if user_input.lower() == "exit":
                print("\nExiting the program.")
                break

            elif user_input.lower() == "r":
                print("\nRefreshing the data...\n")
                final_df = None  # Reset DataFrame to fetch fresh data

            elif user_input:
                print(f"\n🔍 Searching for car park number '{user_input}'...\n")
                search_results = search_carpark(final_df, user_input.upper())
                display_search_results(search_results)

            else:
                print("Invalid input. Please enter a valid car park number.")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")

        except KeyboardInterrupt:
            print("\nUser interrupted the program. Exiting gracefully.")
            break

        except Exception as e:
            print(f"Unexpected error occurred: {e}")


if __name__ == "__main__":
    main_loop()
