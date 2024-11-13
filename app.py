import streamlit as st
import pandas as pd
from opencage.geocoder import OpenCageGeocode
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Get the API key from environment variables
opencage_api_key = os.getenv('OPENCAGE_API_KEY')

# Check if the API key was loaded successfully
if not opencage_api_key:
    st.error("API Key for OpenCage is not available. Please check your .env file.")
    st.stop()

# Initialize the OpenCage Geocoder with the API key
geocoder = OpenCageGeocode(opencage_api_key)

# Function to get address from latitude and longitude and generate Google Maps link
def get_address(lat, lon):
    try:
        result = geocoder.reverse_geocode(lat, lon)
        if result and len(result):
            address = result[0]['formatted']
        else:
            address = 'Address not found'

        # Generate Google Maps link
        google_maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        
        return address, google_maps_link
    except Exception as e:
        return f'Error: {str(e)}', None

# Streamlit App
def main():
    st.title("SEARS Geocode: Locating Technician's Punch Locations")
    st.write("This app converts latitude and longitude coordinates to addresses and generates Google Maps links.")
    st.divider()
    st.write("Please upload a CSV file with latitude and longitude columns.")

    # File uploader for CSV
    uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

    if uploaded_file is not None:
        try:
            # Try to read the uploaded CSV file
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Error reading the CSV file: {str(e)}")
            return

        # Convert column names to lowercase and strip whitespace for case-insensitive checks
        lower_columns = [col.lower().strip() for col in df.columns]

        # Detect latitude and longitude columns
        latitude_column = [col for col in df.columns if "latitude" in col.lower().strip()]
        longitude_column = [col for col in df.columns if "longitude" in col.lower().strip()]

        # Assuming only one match for each
        latitude_column = latitude_column[0] if latitude_column else None
        longitude_column = longitude_column[0] if longitude_column else None

        # Ensure both latitude and longitude are found
        if latitude_column and longitude_column:
            st.write(f"Detected 'latitude' column: {latitude_column}")
            st.write(f"Detected 'longitude' column: {longitude_column}")

            try:
                # Convert all columns except latitude and longitude to strings
                for col in df.columns:
                    if col != latitude_column and col != longitude_column:
                        df[col] = df[col].astype(str)

                # Ensure latitude and longitude remain numeric
                df[latitude_column] = pd.to_numeric(df[latitude_column], errors='coerce')
                df[longitude_column] = pd.to_numeric(df[longitude_column], errors='coerce')

                st.write("Preview of uploaded CSV:")
                st.write(df.head())

                # Progress bar
                progress_bar = st.progress(0)

                # Get addresses and Google Maps links for each row in the CSV
                addresses = []
                google_maps_links = []
                total_rows = len(df)
                for index, row in df.iterrows():
                    lat, lon = row[latitude_column], row[longitude_column]
                    address, google_maps_link = get_address(lat, lon)
                    addresses.append(address)
                    google_maps_links.append(google_maps_link)

                    # Update progress bar
                    progress_bar.progress((index + 1) / total_rows)

                # Add addresses and Google Maps links to DataFrame
                df['address'] = addresses
                df['google_maps_link'] = google_maps_links

                # Display updated DataFrame
                st.write("Updated CSV with addresses and Google Maps links:")
                st.write(df.head())

                # Option to download the updated CSV
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download CSV with Addresses and Google Maps Links",
                    data=csv,
                    file_name='updated_addresses_with_links.csv',
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


# import streamlit as st
# import pandas as pd
# from opencage.geocoder import OpenCageGeocode
# import os
# from dotenv import load_dotenv

# # Load the environment variables from .env file
# load_dotenv()

# # Get the API key from environment variables
# opencage_api_key = os.getenv('OPENCAGE_API_KEY')

# # Check if the API key was loaded successfully
# if not opencage_api_key:
#     st.error("API Key for OpenCage is not available. Please check your .env file.")
#     st.stop()

# # Initialize the OpenCage Geocoder with the API key
# geocoder = OpenCageGeocode(opencage_api_key)

# # Function to get address from latitude and longitude and generate Google Maps link
# def get_address(lat, lon):
#     try:
#         result = geocoder.reverse_geocode(lat, lon)
#         if result and len(result):
#             address = result[0]['formatted']
#         else:
#             address = 'Address not found'

#         # Generate Google Maps link
#         google_maps_link = f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
        
#         return address, google_maps_link
#     except Exception as e:
#         return f'Error: {str(e)}', None

# # Streamlit App
# def main():
#     st.title("SEARS Geocode: Locating Technician's punch locations")
#     st.write("This app converts latitude and longitude coordinates to addresses and generates Google Maps links.")
#     st.divider()
#     st.write("Please upload a CSV file with latitude and longitude columns.")

#     # File uploader for CSV
#     uploaded_file = st.file_uploader("Upload your CSV file", type=['csv'])

#     if uploaded_file is not None:
#         try:
#             # Try to read the uploaded CSV file
#             df = pd.read_csv(uploaded_file)
#         except Exception as e:
#             st.error(f"Error reading the CSV file: {str(e)}")
#             return

#         # Convert column names to lowercase for case-insensitive checks
#         lower_columns = [col.lower() for col in df.columns]

#         # Detect latitude and longitude columns
#         latitude_column = None
#         longitude_column = None

#         for col in lower_columns:
#             if "latitude" in col:
#                 latitude_column = df.columns[lower_columns.index(col)]
#             if "longitude" in col:
#                 longitude_column = df.columns[lower_columns.index(col)]

#         # Ensure both latitude and longitude are found
#         if latitude_column and longitude_column:
#             st.write(f"Detected 'latitude' column: {latitude_column}")
#             st.write(f"Detected 'longitude' column: {longitude_column}")

#             try:
#                 # Convert all columns except latitude and longitude to strings
#                 df = df.applymap(lambda x: str(x) if not pd.api.types.is_numeric_dtype(x) or x.name not in [latitude_column, longitude_column] else x)

#                 # Ensure latitude and longitude remain numeric
#                 df[latitude_column] = pd.to_numeric(df[latitude_column], errors='coerce')
#                 df[longitude_column] = pd.to_numeric(df[longitude_column], errors='coerce')

#                 st.write("Preview of uploaded CSV:")
#                 st.write(df.head())

#                 # Progress bar
#                 progress_bar = st.progress(0)

#                 # Get addresses and Google Maps links for each row in the CSV
#                 addresses = []
#                 google_maps_links = []
#                 total_rows = len(df)
#                 for index, row in df.iterrows():
#                     lat, lon = row[latitude_column], row[longitude_column]
#                     address, google_maps_link = get_address(lat, lon)
#                     addresses.append(address)
#                     google_maps_links.append(google_maps_link)

#                     # Update progress bar
#                     progress_bar.progress((index + 1) / total_rows)

#                 # Add addresses and Google Maps links to DataFrame
#                 df['address'] = addresses
#                 df['google_maps_link'] = google_maps_links

#                 # Display updated DataFrame
#                 st.write("Updated CSV with addresses and Google Maps links:")
#                 st.write(df.head())

#                 # Option to download the updated CSV
#                 csv = df.to_csv(index=False).encode('utf-8')
#                 st.download_button(
#                     label="Download CSV with Addresses and Google Maps Links",
#                     data=csv,
#                     file_name='updated_addresses_with_links.csv',
#                     mime='text/csv'
#                 )
#             except Exception as e:
#                 st.error(f"Error during processing: {str(e)}")
#         else:
#             st.error("CSV must contain columns for latitude and longitude.")
#     else:
#         st.info("Upload a CSV file to begin.")

# if __name__ == '__main__':
#     main()
