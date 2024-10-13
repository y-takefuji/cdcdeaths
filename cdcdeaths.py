import os
import sys
import requests
import pandas as pd
import matplotlib.pyplot as plt

def download_csv(url, filename):
    """
    Downloads a CSV file from the specified URL if it does not already exist.

    Parameters:
        url (str): The URL to download the CSV from.
        filename (str): The local filename to save the CSV as.

    Returns:
        None
    """
    if os.path.exists(filename):
        print(f"'{filename}' already exists. Skipping download.")
        return
    try:
        print(f"Downloading '{filename}' from {url}...")
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise HTTPError for bad responses
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print(f"Downloaded '{filename}' successfully.")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred while downloading '{filename}': {http_err}")
        sys.exit(1)
    except Exception as err:
        print(f"An error occurred while downloading '{filename}': {err}")
        sys.exit(1)

def visualize_covid_deaths(filename, output_image):
    """
    Reads the CSV file, filters the data, aggregates COVID-19 deaths by age group,
    and visualizes the data using a black solid-line graph.

    Parameters:
        filename (str): The path to the CSV file.
        output_image (str): The filename to save the resulting graph.

    Returns:
        None
    """
    # Define the age groups in the desired order
    age_groups = [
        "Under 1 year",
        "1-4 years",
        "5-14 years",
        "15-24 years",
        "25-34 years",
        "35-44 years",
        "45-54 years",
        "55-64 years",
        "65-74 years",
        "75-84 years",
        "85 years and over"
    ]
    
    # Read the CSV file
    try:
        print(f"Reading data from '{filename}'...")
        df = pd.read_csv(filename)
        print("CSV file loaded successfully.")
    except FileNotFoundError:
        print(f"Error: '{filename}' file not found.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: '{filename}' is empty.")
        sys.exit(1)
    except pd.errors.ParserError:
        print(f"Error: '{filename}' is malformed or contains parsing errors.")
        sys.exit(1)
    
    # Display the initial number of rows (optional)
    print(f"Total rows in the dataset: {len(df)}")
    
    # Filter the DataFrame based on the specified criteria
    filtered_df = df[
        (df['Start Date'] == "01/01/2020") &
        (df['End Date'] == "09/23/2023") &
        (df['State'] == "United States") &
        (df['Sex'] == "All Sexes") &
        (df['Age Group'].isin(age_groups))
    ]
    
    # Check if the filtered DataFrame is empty
    if filtered_df.empty:
        print("No data available for the specified filters.")
        sys.exit(1)
    
    # Ensure 'COVID-19 Deaths' is of integer type
    # Handle potential non-numeric entries by coercing errors to NaN
    filtered_df['COVID-19 Deaths'] = pd.to_numeric(filtered_df['COVID-19 Deaths'], errors='coerce')
    
    # Handle any potential NaN values after conversion
    filtered_df = filtered_df.dropna(subset=['COVID-19 Deaths'])
    
    # Convert 'COVID-19 Deaths' to integer
    filtered_df['COVID-19 Deaths'] = filtered_df['COVID-19 Deaths'].astype(int)
    
    # Group the data by 'Age Group' and sum the deaths
    grouped_df = filtered_df.groupby('Age Group')['COVID-19 Deaths'].sum().reindex(age_groups, fill_value=0)
    
    # Display the aggregated data (optional)
    print("Aggregated COVID-19 Deaths by Age Group:")
    print(grouped_df)
    
    # Create the black solid-line graph
    plt.figure(figsize=(14, 8))
    
    plt.plot(
        grouped_df.index,
        grouped_df.values,
        marker='o',
        linestyle='-',
        color='black',  # Set line color to black
        linewidth=2,
        markersize=6
    )
    
    # Add data labels for each point
    for x, y in zip(grouped_df.index, grouped_df.values):
        plt.text(
            x,
            y + max(grouped_df.values)*0.01,  # Slightly above the point
            str(y),
            ha='center',
            va='bottom',
            fontsize=10
        )
    
    # Customize the graph
    plt.xlabel('Age Group', fontsize=14)
    plt.ylabel('Total COVID-19 Deaths', fontsize=14)
    plt.title('Total COVID-19 Deaths by Age Group (01/01/2020 - 09/23/2023)', fontsize=16)
    plt.xticks(rotation=90, fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(True, which='both', linestyle='--', linewidth=0.5, alpha=0.7)
    
    plt.tight_layout()
    
    # Save the graph to a file
    plt.savefig(output_image, dpi=300)
    print(f"Graph has been saved as '{output_image}'.")
    
    # Display the graph
    plt.show()

def main():
    # URL to download the CSV file
    csv_url = "https://data.cdc.gov/api/views/9bhg-hcku/rows.csv"
    csv_filename = "rows.csv"
    output_image = "result.png"
    
    # Download the CSV file if it does not exist
    download_csv(csv_url, csv_filename)
    
    # Visualize the data
    visualize_covid_deaths(csv_filename, output_image)

if __name__ == "__main__":
    main()
