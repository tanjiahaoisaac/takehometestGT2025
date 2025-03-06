import pandas as pd
from datetime import datetime, timedelta
import os


def get_event_photo_urls(photo_list):
    """
    Extract all photo URLs from the photo list and return them as a comma-separated string.
    If the list is empty or None, return 'NA'.
    
    Args:
        photo_list (list): List of photo objects that contain URL details.

    Returns:
        str: Comma-separated string of photo URLs or 'NA' if no URLs are available.
    """
    if photo_list and len(photo_list) > 0:
        photo_urls = [photo.get('photo', {}).get('url', 'NA') for photo in photo_list]
        return ', '.join(photo_urls)  # Join all URLs with a comma
    return 'NA'


def filter_events_by_month(events_df, year, month):
    """
    Filter events that overlap with the specified month and year.
    Includes events that start or end in the specified month and year or have an event during that month.
    
    Args:
        events_df (pandas dataframe): dataframe containing event data from normlisation function.
        year (int): The year to filter by.
        month (int): The month to filter by.

    Returns:
        pandas dataframe: Filtered dataframe containing events that overlap with the specified month and year.
    """
    # Define the start and end of the specified month and year as datetime objects
    month_start = datetime(year, month, 1)
    
    # Determine the last day of the specified month
    if month == 12:  # If December, the next month will be January
        month_end = datetime(year + 1, 1, 1) - timedelta(days=1)
    else:
        month_end = datetime(year, month + 1, 1) - timedelta(days=1)

    # Convert start_date and end_date columns to datetime objects, just in case they are not already
    events_df['start_date'] = pd.to_datetime(events_df['start_date'], errors='coerce')
    events_df['end_date'] = pd.to_datetime(events_df['end_date'], errors='coerce')

    # Filter events that overlap with the specified month
    filtered_events = events_df[
        (events_df['start_date'] <= month_end) & (events_df['end_date'] >= month_start)
    ]

    return filtered_events


def extract_event_data(events_df, restaurant_df, year, month, output_path):
    """
    Extract relevant event fields and join with restaurant data to create the final dataframe.
    This function will save the resulting dataframe to a CSV file at the given output path.

    Args:
        events_df (pandas dataframe): dataframe containing event data from normalisation function.
        restaurant_df (pandas dataframe): dataframe containing restaurant data.
        year (int): The year to filter events by.
        month (int): The month to filter events by.
        output_path (str): Path to save the final CSV file.

    Returns:
        pandas dataframe: The final dataframe containing event and restaurant data for the specified month.
    """
    # Filter events by month
    month_events = filter_events_by_month(events_df, year, month)

    # Extract necessary columns and process photos
    month_events['photo_url'] = month_events['photos'].apply(lambda x: get_event_photo_urls(x))  
    month_events['restaurant_name'] = month_events['restaurant_res_id'].apply(
        lambda res_id: restaurant_df.loc[restaurant_df['id'] == res_id, 'name'].values[0]
        if not restaurant_df.loc[restaurant_df['id'] == res_id].empty else 'NA'
    )

    # Select final columns to create the new dataframe
    final_df = month_events[['event_id', 'restaurant_res_id', 'restaurant_name', 'photo_url', 'title', 'start_date', 'end_date']]

    # Ensure any missing value is filled with 'NA'
    final_df = final_df.fillna('NA')

    # Export the dataframe to CSV
    os.makedirs(output_path, exist_ok=True)
    final_df.to_csv(os.path.join(output_path, 'filtered_restaurant_events.csv'), index=False)


    return final_df
