import pandas as pd
import os


def load_country_codes(country_code_file_path):
    """
    Load the country codes from the provided xlsx file.

    Args:
        country_code_file_path (str): Path to the 'Country-Code.xlsx' file.

    Returns:
        list: List of country codes.
        dict: Mapping of country codes to country names.
    """
    country_codes_df = pd.read_excel(country_code_file_path)
    country_code_array = country_codes_df['Country Code'].tolist()
    country_mapping = country_codes_df.set_index('Country Code')['Country'].to_dict()

    return country_code_array, country_mapping


def filter_restaurants_by_country(df, country_code_array):
    """
    Filter the restaurants data based on the valid country codes.

    Args:
        df (pandas dataframe): The restaurant details from normalise function.
        country_code_array (list): List of valid country codes.

    Returns:
        pandas dataframe: Filtered dataframe with valid countries.
    """
    return df[df['country_id'].isin(country_code_array)]


def add_country_name(df, country_mapping):
    """
    Add the 'Country' column to the dataframe by mapping country codes to country names.

    Args:
        df (pandas dataframe): The filtered restaurant data.
        country_mapping (dict): Mapping of country codes to country names.

    Returns:
        pandas dataframe: dataframe with added 'Country' column.
    """
    df['Country Name'] = df['country_id'].map(country_mapping)
    return df


def select_and_rename_columns(df, event_df):
    """
    Select relevant columns and rename them to the required names, 
    also adding the earliest event start date if available.

    Args:
        df (pandas dataframe): The restaurant details from normalise function.
        event_df (pandas dataframe): The events data for the restaurants.

    Returns:
        pandas dataframe: dataframe with selected and renamed columns, including the earliest event start date.
    """
    def get_earliest_event_date(row):
        # If 'zomato_events' is not NA
        if row['zomato_events'] != 'NA' and isinstance(row['zomato_events'], list) and len(row['zomato_events']) > 0:
            # Find the earliest start date from event_df
            restaurant_res_id = row['id']
            events = event_df[event_df['restaurant_res_id'] == restaurant_res_id]
            if not events.empty:
                earliest_event = events['start_date'].min()
                return earliest_event
        return 'NA'  # If no event or event is NA

    df['Event Start Date'] = df.apply(get_earliest_event_date, axis=1)

    # Select the relevant columns from the original restaurant DataFrame
    df_selected = df[['id', 'name', 'Country Name', 'city', 'votes', 'aggregate_rating', 'cuisines', 'Event Start Date']]

    # Rename the columns to the required names
    df_selected = df_selected.rename(columns={
        'id': 'Restaurant Id',
        'name': 'Restaurant Name',
        'Country Name': 'Country',
        'city': 'City',
        'votes': 'User Rating Votes',
        'aggregate_rating': 'User Aggregate Rating',
        'cuisines': 'Cuisines',
        'Event Start Date': 'Event Date'
    })

    # Optionally convert 'User Aggregate Rating' to float if it's not already
    df_selected['User Aggregate Rating'] = df_selected['User Aggregate Rating'].astype(float)

    return df_selected


def restaurant_details_processing(df, event_df, country_code_file_path, output_path):
    """
    Process the restaurant details data.
    Only include restaurants with matching Country Codes from the provided Country-Code.xlsx file.
    
    Extract the following fields:
    ● Restaurant Id
    ● Restaurant Name
    ● Country
    ● City
    ● User Rating Votes
    ● User Aggregate Rating (as float)
    ● Cuisines
    ● Event Date
    
    And export the processed data to a CSV file.

    Args:
        df (pandas dataframe): The restaurant details data from normalise function.
        country_code_file_path (str): Path to the 'Country-Code.xlsx' file containing valid country codes.
        output_path (str): Path where the processed CSV file should be saved.

    Returns:
        pandas dataframe: The processed restaurant details data.
    """
    # Load country codes
    country_code_array, country_mapping = load_country_codes(country_code_file_path)

    # Filter restaurants based on valid country codes
    df_filtered = filter_restaurants_by_country(df, country_code_array)

    # Add 'Country' column to the dataframe
    df_with_country = add_country_name(df_filtered, country_mapping)

    # Select relevant columns and rename them
    df_selected = select_and_rename_columns(df_with_country, event_df)

    # Export the processed data to CSV
    os.makedirs(output_path, exist_ok=True)
    df_selected.to_csv(os.path.join(output_path, 'processed_restaurant_data.csv'), index=False)

    return df_selected
