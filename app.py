import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

# Initialize the Nominatim geolocator
geolocator = Nominatim(user_agent="geoapiExercises")

# Function to get address from latitude and longitude with error handling
def get_address(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language='en')
        return location.address if location else 'Address not found'
    except GeocoderTimedOut:
        return 'Geocoding Timed Out'
    except GeocoderServiceError:
        return 'Geocoding Service Error'
    except Exception as e:
        return f'Error: {str(e)}'

# Streamlit App
def main():
    st.title("Geocode CSV: Convert Latitude & Longitude to Address")

    # File uploader for CSV
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

    if uploaded_file is not None:
        try:
            # Try to read the uploaded CSV file
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading the CSV file: {str(e)}")
            return

        # Convert column names to lowercase for case-insensitive checks
        lower_columns = [col.lower() for col in df.columns]

        # Detect latitude and longitude columns
        latitude_column = None
        longitude_column = None

        for col in lower_columns:
            if "latitude" in col:
                latitude_column = df.columns[lower_columns.index(col)]
            if "longitude" in col:
                longitude_column = df.columns[lower_columns.index(col)]

        # Ensure both latitude and longitude are found
        if latitude_column and longitude_column:
            st.write(f"Detected 'latitude' column: {latitude_column}")
            st.write(f"Detected 'longitude' column: {longitude_column}")

            try:
                # Convert all columns except latitude and longitude to strings
                df = df.applymap(lambda x: str(x) if not pd.api.types.is_numeric_dtype(x) or x.name not in [latitude_column, longitude_column] else x)

                # Ensure latitude and longitude remain numeric
                df[latitude_column] = pd.to_numeric(df[latitude_column], errors='coerce')
                df[longitude_column] = pd.to_numeric(df[longitude_column], errors='coerce')

                st.write("Preview of uploaded CSV:")
                st.write(df.head())

                # Progress bar
                progress_bar = st.progress(0)

                # Get addresses for each row in the CSV
                addresses = []
                total_rows = len(df)
                for index, row in df.iterrows():
                    lat, lon = row[latitude_column], row[longitude_column]
                    address = get_address(lat, lon)
                    addresses.append(address)

                    # Update progress bar
                    progress_bar.progress((index + 1) / total_rows)

                # Add addresses to DataFrame
                df['address'] = addresses

                # Display updated DataFrame
                st.write("Updated CSV with addresses:")
                st.write(df.head())

                # Option to download the updated CSV
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV with Addresses",
                    data=csv,
                    file_name='updated_addresses.csv',
                    mime='text/csv'
                )
            except Exception as e:
                st.error(f"Error during processing: {str(e)}")
        else:
            st.error("CSV must contain columns for latitude and longitude.")
    else:
        st.info("Upload a CSV file to begin.")

if __name__ == '__main__':
    main()
