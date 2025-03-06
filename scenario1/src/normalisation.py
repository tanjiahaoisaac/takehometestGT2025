import pandas as pd


def normalise_data(json_file):
    """
    Normalise the data by:
    1. Extracting the individual restaurant data from the nested JSON structure.
    2. Flattening nested JSON columns (location, user_rating).
    3. Extracting 'zomato_events' into a separate Ddataframe.
    4. Handling missing data by replacing it with 'NA'.
    
    Args:
        json_file (list): The raw JSON data to be normalised, typically 
                          a list of dictionaries representing restaurant data.

    Returns:
        restaurant_df (pandas dataframe): dataframe of restaurant data.
        events_df (pandas dataframe): dataframe of event data for the restaurants.
    """
    restaurant_list = []
    events_list = []

    # Extract individual restaurants and events
    for row in json_file:
        restaurants = row.get("restaurants", [])
        for restaurant in restaurants:
            restaurant_data = restaurant["restaurant"]
            restaurant_list.append(restaurant_data)

            # Extract events for the current restaurant
            zomato_events = restaurant_data.get("zomato_events", [])
            for event in zomato_events:
                event_data = {
                    'event_id': event.get('event', {}).get('event_id', 'NA'),
                    'title': event.get('event', {}).get('title', 'NA'),
                    'description': event.get('event', {}).get('description', 'NA'),
                    'start_date': event.get('event', {}).get('start_date', 'NA'),
                    'end_date': event.get('event', {}).get('end_date', 'NA'),
                    'start_time': event.get('event', {}).get('start_time', 'NA'),
                    'end_time': event.get('event', {}).get('end_time', 'NA'),
                    'event_category': event.get('event', {}).get('event_category', 'NA'),
                    'photos': event.get('event', {}).get('photos', 'NA'),
                    'restaurant_res_id': restaurant_data.get('id', 'NA'),  #FK to the correct restaurant
                }
                events_list.append(event_data)

    # Convert to dataframe for restaurants
    restaurant_df = pd.DataFrame(restaurant_list)

    #Normalise 'location' column 
    if 'location' in restaurant_df.columns:
        location_df = pd.json_normalize(restaurant_df['location'])
        restaurant_df = pd.concat([restaurant_df.drop(columns=['location']), location_df], axis=1)

    # Normalise 'user_rating' column 
    if 'user_rating' in restaurant_df.columns:
        user_rating_df = pd.json_normalize(restaurant_df['user_rating'])
        restaurant_df = pd.concat([restaurant_df.drop(columns=['user_rating']), user_rating_df], axis=1)

    # Convert to dataframe for events
    events_df = pd.DataFrame(events_list)

    # Replace missing values with 'NA'
    restaurant_df.fillna('NA', inplace=True)
    events_df.fillna('NA', inplace=True)

    return restaurant_df, events_df
