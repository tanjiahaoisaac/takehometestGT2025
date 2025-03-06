import pandas as pd

def analyze_rating_thresholds(df):
    """
    Analyse the relationship between aggregate ratings and rating texts.
    Categorises the ratings into Excellent, Very Good, Good, Average, and Poor
    and calculates the min, max, and range (max - min) of aggregate ratings for each category.

    Based on the above range found, re-categorises the ratings(foreign rating text) in the dataframe that do not fall into the above categories.
    Sort out unmapped ratings
    
    Args:
        df (dataframe): Normalised dataframe containing restaurant ratings, including 'aggregate_rating' and 'rating_text'.
    
    Returns:
        pandas dataframe: dataframe containing the min, max, and range of aggregate ratings for each category,
                          ordered by Poor, Average, Good, Very Good, and Excellent.
        pandas dataframe: dataframe containing the mapping of foreign rating_text to English rating_text.
        pandas dataframe: dataframe containing the rows that could not be mapped to an English rating.
    """
    try:
        # Check if the input dataframe has the necessary columns
        if 'rating_text' not in df.columns or 'aggregate_rating' not in df.columns:
            raise ValueError("The dataframe must contain 'rating_text' and 'aggregate_rating' columns.")

        # Define the valid categories in the desired order
        valid_rating_categories = ['Poor', 'Average', 'Good', 'Very Good', 'Excellent']
        
        # Filter rows where rating_text is in the valid categories
        valid_ratings_df = df[df['rating_text'].isin(valid_rating_categories)]
        
        # Filter rows that are not in the valid categories
        invalid_ratings_df = df[~df['rating_text'].isin(valid_rating_categories)]
        
        # Group by rating_text and calculate min and max aggregate_rating for each category
        category_stats = valid_ratings_df.groupby('rating_text')['aggregate_rating'].agg(['min', 'max']).reset_index()

        # Ensure min and max are cast to float
        category_stats['max'] = category_stats['max'].astype(float)
        category_stats['min'] = category_stats['min'].astype(float)

        # Calculate the range as max - min
        category_stats['range'] = category_stats['max'] - category_stats['min']

        # Ensure the categories are ordered as Poor, Average, Good, Very Good, and Excellent
        category_stats['rating_text'] = pd.Categorical(category_stats['rating_text'], categories=valid_rating_categories, ordered=True)
        
        # Sort by the custom category order
        category_stats = category_stats.sort_values('rating_text')

        # Create the rating thresholds dynamically based on the min/max of each valid category
        rating_thresholds = {}
        for _, row in category_stats.iterrows():
            rating_text = row['rating_text']
            rating_thresholds[rating_text] = (row['min'], row['max'])

        # This function will map an aggregate_rating to the appropriate English rating text
        def map_rating_to_text(aggregate_rating):
            try:
                # Ensure the aggregate_rating is cast to float before comparison
                aggregate_rating = float(aggregate_rating)
                for rating, (min_rating, max_rating) in rating_thresholds.items():
                    if min_rating <= aggregate_rating <= max_rating:
                        return rating
                return None  # In case no mapping is found
            except ValueError as e:
                raise ValueError(f"Invalid aggregate_rating value: {aggregate_rating}. Error: {e}")
        
        # Find the rows with invalid ratings and map them to valid English ratings
        invalid_ratings_df['mapped_rating_text'] = invalid_ratings_df['aggregate_rating'].apply(map_rating_to_text)
        
        # Rows that could not be mapped to an English rating
        failed_mapping_df = invalid_ratings_df[invalid_ratings_df['mapped_rating_text'].isna()]

        # Rows that were successfully mapped to English categories
        successfully_mapped_df = invalid_ratings_df[~invalid_ratings_df['mapped_rating_text'].isna()]

        # Create a DataFrame with the mapping from aggregate_rating to rating_text
        successful_translated_text = successfully_mapped_df[['rating_text', 'aggregate_rating', 'mapped_rating_text']]

        return category_stats, successful_translated_text, failed_mapping_df

    except KeyError as e:
        raise KeyError(f"Missing expected column in the dataframe: {e}")
    except ValueError as e:
        raise ValueError(f"Data validation error: {e}")
    except TypeError as e:
        raise TypeError(f"Type error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")
