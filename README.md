# SEARS-Tech-Geolocator

This is a **Streamlit web application** that allows users to upload a CSV file containing latitude and longitude columns, converts the coordinates to human-readable addresses using reverse geocoding, and provides the option to download the updated CSV with the address added as a new column.

## Features
- Upload a CSV file with **latitude** and **longitude** columns.
- Automatically detect latitude and longitude columns in a case-insensitive manner.
- Retrieve the corresponding address for each pair of coordinates.
- Download the updated CSV file with the **address** column appended.
- Progress bar to indicate processing status.

## Demo
Once deployed on Streamlit Cloud, you can access the live version of the app here: [Your App Link]([https://your-app-link.streamlit.app](https://sears-tech-geolocator-v1.streamlit.app/)).

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name

2. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    venv\Scripts\activate     # For Windows
    ```

3. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Requirements

- **Python 3.x**
- **Streamlit** for running the web application.
- **Pandas** for handling CSV file operations.
- **OpenCage** for reverse geocoding latitude and longitude to addresses.
- **python-dotenv** for managing environment variables.

To install these dependencies manually, you can run:

```bash
pip install streamlit pandas opencage python-dotenv
```

## Running the App Locally
1. Make sure all dependencies are installed.
2. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
3. Open a browser and go to http://localhost:8501 to view the app.

## Usage
- **Upload CSV**: The app expects a CSV file with at least two columns for latitude and longitude. The column names are detected automatically, so there is no need to follow strict naming conventions.

- **Geocoding**: Once the file is uploaded, the app processes each latitude and longitude pair, converts it to a human-readable address, and adds it as a new column to the CSV.

- **Download**: After processing, you can download the updated CSV with the newly added **address** column.

## Example CSV Input

| service_order_number | latitude  | longitude  |
|----------------------|-----------|------------|
| 12345                | 40.748817 | -73.985428 |
| 67890                | 51.507351 | -0.127758  |

## Example CSV Output

| service_order_number | latitude  | longitude  | address                              |
|----------------------|-----------|------------|--------------------------------------|
| 12345                | 40.748817 | -73.985428 | Empire State Building, New York, USA |
| 67890                | 51.507351 | -0.127758  | London, United Kingdom               |


## Deployment

This app can be easily deployed to **Streamlit Cloud** or any other hosting platform that supports Streamlit. Follow the deployment steps outlined below:

1. **Sign in to Streamlit Cloud**: [Streamlit Cloud](https://streamlit.io/cloud)
2. **Connect GitHub repo**: Deploy the app by selecting the repository containing this code.
3. **Set up requirements**: Ensure the `requirements.txt` file is correctly set up with the necessary dependencies (`pandas`, `geopy`, `streamlit`).

## Contributing

Feel free to submit issues or pull requests if you find any bugs or want to improve the functionality of the app.

