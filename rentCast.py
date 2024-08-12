import requests
import json
import boto3
from botocore.exceptions import NoCredentialsError

# Get RentCast API and AWS access keys
with open("rentcast_api.txt", "r") as f:
    rentcast_api = f.readline().strip()

with open("access_key.txt", "r") as f:
    access_key = f.readline().strip()

with open("secret_access_key.txt", "r") as f:
    secret_access_key = f.readline().strip()

# Your RentCast API endpoint and parameters
rentcast_url = "https://api.rentcast.io/v1/markets?zipCode=29611&historyRange=6"
headers = {
    "accept": "application/json",
    "X-Api-Key": rentcast_api
}

# Make the API request
response = requests.get(rentcast_url, headers=headers)

if response.status_code == 200:
    # Parse the JSON response
    rentcast_data = response.json()

    # Optional: save locally before uploading to S3
    with open('rentcast_data.json', 'w') as json_file:
        json.dump(rentcast_data, json_file, indent=4)
else:
    print(f"Failed to retrieve data: {response.status_code}")

# Initialize the S3 client
s3 = boto3.client(
    's3',
    aws_access_key_id = access_key,
    aws_secret_access_key = secret_access_key,
    region_name = 'us-east-2'
)

# Your S3 bucket name and the target file name
bucket_name = 'real-estate-data-crunchybucket'
s3_file_name = 'rentcast_data.json'

try:
    # Upload the file
    s3.upload_file('rentcast_data.json', bucket_name, s3_file_name)
    print(f"Successfully uploaded {s3_file_name} to S3 bucket {bucket_name}.")
except FileNotFoundError:
    print("The file was not found")
except NoCredentialsError:
    print("Credentials not available")

