import streamlit as st
import pandas as pd
from src.fetch_restaurant_data import fetch_restaurant_data_from_api
from src.details_processing import restaurant_details_processing
from src.normalisation import normalise_data
from src.filter_events import extract_event_data
from src.rating_analyser import analyze_rating_thresholds
import io



# Title and description
st.title('Restaurant Data Analysis Tool')
st.write("GT Take home scenario 1")
st.write("By Isaac Tan")
st.write("Task 1. Restaurant Details")
st.write("Task 2. Events")
st.write("Task 3. Ratings")
st.write("###")
# Fetching restaurant data from API
data = fetch_restaurant_data_from_api("https://raw.githubusercontent.com/Papagoat/brain-assessment/main/restaurant_data.json")

# Normalize the data
df_normal, df_events = normalise_data(data)

# Process restaurant details
df_details = restaurant_details_processing(df_normal, df_events, 'data/Country-Code.xlsx', 'output/')

st.subheader("1. Restaurant Details Data")
st.dataframe(df_details)

if df_details is not None:
    # Create a download button
    csv = df_details.to_csv(index=False)  # Convert the dataframe to CSV format
    st.download_button(
        label="Download Restaurant Details Data as CSV",  # Text on the button
        data=csv,  # Data to be downloaded
        file_name=f"restaurant_details_data.csv",  # File name
        mime="text/csv",  # MIME type for CSV
        use_container_width=True,  # Make button span the width of the container
    )

st.write("###")

st.subheader("Task 2. Events")
# Input fields for year and month selection
year = st.number_input("Enter year", min_value=2010, max_value=2100, value=2019)
month = st.number_input("Enter month", min_value=1, max_value=12, value=4)

# Filter events based on the selected year and month
df_month_events = extract_event_data(df_events, df_normal, year, month, 'output/')

# Analyze rating thresholds
scores_range, foreign_text_to_english_map, fail = analyze_rating_thresholds(df_normal)

st.subheader(f"Event Data for {year}-{month}")
st.dataframe(df_month_events)

# Check if df_month_events is not None before attempting to convert to CSV
if df_month_events is not None:
    # Convert the dataframe to CSV format
    csv = df_month_events.to_csv(index=False)
    
    # Create a download button
    st.download_button(
        label="Download Event Data as CSV",  # Text on the button
        data=csv,  # Data to be downloaded
        file_name=f"event_data_{year}_{month}.csv",  # File name
        mime="text/csv",  # MIME type for CSV
        use_container_width=True,  # Make button span the width of the container
    )

        # Loop through each row of the dataframe and display the data
    for index, row in df_month_events.iterrows():
        # Display restaurant name with rich text (markdown)
        st.markdown(f"### {row['Restaurant Name']}")  # Render restaurant name as markdown for rich text
        
        # Display event title (rich text)
        st.markdown(f"**Event Title:** {row['Event Title']}") 
        
        # Handle multiple photo URLs (comma-separated) and check for "NA"
        photo_urls = row['Photo URL(s)'].split(',')
        
        if len(photo_urls) > 1:
            # If multiple photos exist, use columns for left-right layout
            cols = st.columns(len(photo_urls))
            for i, url in enumerate(photo_urls):
                if url.strip() != "NA":  # Skip if photo_url is "NA"
                    cols[i].image(url, width=200)  # Smaller size for images
        else:
            # If there's only one photo, display it normally
            if photo_urls[0].strip() != "NA":
                st.image(photo_urls[0], width=200)  # Smaller size for single image
        
        # Display event start and end date
        st.write(f"**Start Date:** {row['Start Date']}")
        st.write(f"**End Date:** {row['End Date']}")

        # Add a separator (border) between events
        st.markdown("---")

else:
    st.warning("No event data available to download.")



# Rating Threshold Analysis section
st.subheader("Task 2. Ratings")
st.write("Score Range:")
st.dataframe(scores_range)
st.write("Foreign Text to English Map:")
st.dataframe(foreign_text_to_english_map)

