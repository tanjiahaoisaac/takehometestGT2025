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
        df (pandas dataframe): The restaurant details data.
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


def select_and_rename_columns(df):
    """
    Select relevant columns and rename them to the required names.

    Args:
        df (pandas dataframe): The restaurant details data.

    Returns:
        pandas dataframe: dataframe with selected and renamed columns.
    """
    # Select the relevant columns
    df_selected = df[['id', 'name', 'Country Name', 'city', 'votes', 'aggregate_rating', 'cuisines', 'event.start_date']]

    # Rename the columns to the required names
    df_selected = df_selected.rename(columns={
        'id': 'Restaurant Id',
        'name': 'Restaurant Name',
        'Country Name': 'Country',
        'city': 'City',
        'votes': 'User Rating Votes',
        'aggregate_rating': 'User Aggregate Rating',
        'cuisines': 'Cuisines',
        'event.start_date': 'Event Date'
    })

    # Optionally convert 'User Aggregate Rating' to float if it's not already
    df_selected['User Aggregate Rating'] = df_selected['User Aggregate Rating'].astype(float)

    return df_selected


def export_to_csv(df, output_path):
    """
    Export the processed dataframe to a CSV file.

    Args:
        df (pandas dataframe): The processed dataframe.
        output_path (str): Path where the processed CSV file should be saved.
    """
    os.makedirs(output_path, exist_ok=True)
    df.to_csv(os.path.join(output_path, 'processed_restaurant_data.csv'), index=False)


def restaurant_details_processing(df, country_code_file_path, output_path):
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
        df (pandas dataframe): The restaurant details data.
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
    df_selected = select_and_rename_columns(df_with_country)

    # Export the processed data to CSV
    export_to_csv(df_selected, output_path)

    return df_selected
