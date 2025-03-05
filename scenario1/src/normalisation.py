import pandas as pd

def normalise_data(df):
    """
    Normalise the data by:
    1. Flattening nested JSON columns (location, user_rating, zomato_events).
    2. Handling missing data by replacing it with 'NA'.
    3. Converting date columns to datetime objects.
    4. Removing unnecessary prefixes from column names.
    
    Args:
        df: The raw pandas dataframe to be normalized.
    
    Returns:
        pandas dataframe: The normalised and polished dataframe.
    """
    
    #Normalise 'location' column 
    if 'location' in df.columns:
        location_df = pd.json_normalize(df['location'])
        location_df.columns = location_df.columns.str.replace('location.', '')
        df = pd.concat([df.drop(columns=['location']), location_df], axis=1)
    
    #Normalise 'user_rating' column 
    if 'user_rating' in df.columns:
        user_rating_df = pd.json_normalize(df['user_rating'])
        user_rating_df.columns = user_rating_df.columns.str.replace('user_rating.', '')
        df = pd.concat([df.drop(columns=['user_rating']), user_rating_df], axis=1)
    
    #Normalise 'zomato_events' column 
    if 'zomato_events' in df.columns:
        zomato_events_df = pd.json_normalize(df['zomato_events'].explode())
        zomato_events_df.columns = zomato_events_df.columns.str.replace('event.', '')
        df = pd.concat([df.drop(columns=['zomato_events']), zomato_events_df], axis=1)
    
    
    #Fill missing values with 'NA'
    df.fillna('NA', inplace=True)
    
    return df