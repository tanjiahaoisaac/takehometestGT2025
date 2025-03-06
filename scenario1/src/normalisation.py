import pandas as pd

def normalise_data(json_file):
    """
    Normalise the data by:
    1. Extracting the individual restaurant data from the nested JSON structure.
    2. Flattening nested JSON columns (location, user_rating, zomato_events,photos).
    3. Handling missing data by replacing it with 'NA'.
    
    Args:
        json_file (json): The raw json to be normalized.
    
    Returns:
        pandas dataframe: The normalised and polished dataframe.
    """
    restaurant_list = []

    #Row represents some sort of pagination
    #Each row has restaurants dict, which each has many restaurant dict
    #Extract all the individuakl resturants
    for row in json_file:
        restaurants=row.get("restaurants", [])
        for restaurant in restaurants:  
            # Extract actual restaurant data
            restaurant_list.append(restaurant["restaurant"])  

    # Convert to DataFrame
    df = pd.DataFrame(restaurant_list)
    
    #Normalise 'location' column 
    if 'location' in df.columns:
        location_df = pd.json_normalize(df['location'])
        location_df.columns = location_df.columns.str.replace('location.', '')
        df = pd.concat([df.drop(columns=['location']), location_df], axis=1)
    
    #Normalise 'user_rating' column 
    if 'user_rating' in df.columns:
        user_rating_df = pd.json_normalize(df['user_rating'])
        
        df = pd.concat([df.drop(columns=['user_rating']), user_rating_df], axis=1)
    
    #Normalise 'zomato_events' column 
    if 'zomato_events' in df.columns:
        zomato_events_df = pd.json_normalize(df['zomato_events'][0])
        df = pd.concat([df.drop(columns=['zomato_events']), zomato_events_df], axis=1)
    
    #Normalise 'photos' column 
    if 'event.photos' in df.columns:
        photos_df = pd.json_normalize(df['event.photos'][0])
        df = pd.concat([df.drop(columns=['event.photos']), photos_df], axis=1)
    
    
    #Fill missing values with 'NA'
    df.fillna('NA', inplace=True)
    
    return df