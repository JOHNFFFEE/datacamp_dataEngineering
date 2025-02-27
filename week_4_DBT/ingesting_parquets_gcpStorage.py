!pip install google.cloud 

 
from google.cloud import storage

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] =  r"your_gcp_credential_path.json"

# Test GCS client initialization
storage_client = storage.Client()

# List buckets in your project (you can replace with another test action)
buckets = list(storage_client.list_buckets())
print("Buckets:", buckets)

month = datetime.now().strftime("%Y-%m")
print(month)




import os
import requests
from concurrent.futures import ThreadPoolExecutor
from google.cloud import storage

# Define parameters
BASE_URL_YELLOW = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_"
BASE_URL_GREEN = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_"
BASE_URL_FHV = "https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_"
DOWNLOAD_DIR = r"folder_download\nyc"  # Set your download directory path
BUCKET_NAME = "mybucketde"  # Your Google Cloud Storage bucket name

# List of months to download (for each year dataset)
MONTHS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]  # Example months for each year

# Years for the datasets
YEARS = ["2019", "2020"]

# Initialize GCS client
storage_client = storage.Client()

def download_file(url, file_path):
    """Download the file from the CloudFront URL"""
    try:
        print(f"Downloading {url}...")
        response = requests.get(url)
        response.raise_for_status()  # Check if request was successful
        
        # Save the file locally
        with open(file_path, "wb") as file:
            file.write(response.content)
        
        print(f"Downloaded: {file_path}")
        return file_path
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")
        return None

def upload_to_gcs(file_path):
    """Upload the downloaded file to Google Cloud Storage"""
    if file_path:
        # Upload the file to GCS
        bucket = storage_client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"{os.path.basename(file_path)}")
        blob.upload_from_filename(file_path)
        print(f"Uploaded {file_path} to GCS.")

def download_and_process(year, month, dataset_type):
    """Download and upload the dataset for a given year, month, and type"""
    if dataset_type == 'yellow_taxi':
        base_url = BASE_URL_YELLOW
    elif dataset_type == 'green_taxi':
        base_url = BASE_URL_GREEN
    elif dataset_type == 'fhv':
        base_url = BASE_URL_FHV
    else:
        print(f"Unknown dataset type: {dataset_type}")
        return None

    url = f"{base_url}{year}-{month}.parquet"
    file_path = os.path.join(DOWNLOAD_DIR, f"{dataset_type}_{year}-{month}.parquet")
    file_path = download_file(url, file_path)
    return file_path

def main():
    """Main function to manage the download and upload process"""
    # Prepare the months for downloading
    for year in YEARS:
        for month in MONTHS:
            with ThreadPoolExecutor(max_workers=4) as executor:
                # Yellow Taxi (2019 and 2020)
                executor.submit(download_and_process, year, month, "yellow_taxi")
                # Green Taxi (2019 and 2020)
                executor.submit(download_and_process, year, month, "green_taxi")
                # For Hire Vehicle (2019)
                if year == "2019":
                    executor.submit(download_and_process, year, month, "fhv")
                
    # After downloading, upload all files to GCS
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Filter out None values in the file paths
        file_paths = [os.path.join(DOWNLOAD_DIR, f"{dataset_type}_{year}-{month}.parquet")
                      for year in YEARS for month in MONTHS for dataset_type in ["yellow_taxi", "green_taxi", "fhv"]]
        executor.map(upload_to_gcs, filter(None, file_paths))

    print("All files processed and verified.")

if __name__ == "__main__":
    main()





