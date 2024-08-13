import json
import requests
import boto3
from botocore.exceptions import NoCredentialsError
import os

def lambda_handler(event, context):
    # Retrieve environment variables for RentCast API and S3 bucket
    rentcast_api = os.getenv('RENTCAST_API_KEY')
    bucket_name = os.getenv('BUCKET_NAME')
    s3_file_name = 'rentcast_data.json'
    
    # Your RentCast API endpoint and parameters
    zip_code = event.get('zip_code', '29611')  # Default zip code if not provided in event
    history_range = event.get('history_range', '6')  # Default history range if not provided in event
    
    rentcast_url = f"https://api.rentcast.io/v1/markets?zipCode={zip_code}&historyRange={history_range}"
    headers = {
        "accept": "application/json",
        "X-Api-Key": rentcast_api
    }

    # Make the API request
    response = requests.get(rentcast_url, headers=headers)

    if response.status_code == 200:
        # Parse the JSON response
        rentcast_data = response.json()

        # Initialize the S3 client
        s3 = boto3.client('s3')

        try:
            # Upload the data to S3
            s3.put_object(Bucket=bucket_name, Key=s3_file_name, Body=json.dumps(rentcast_data))
            return {
                'statusCode': 200,
                'body': json.dumps(f"Successfully uploaded {s3_file_name} to S3 bucket {bucket_name}.")
            }
        except NoCredentialsError:
            return {
                'statusCode': 403,
                'body': json.dumps("Credentials not available")
            }
    else:
        return {
            'statusCode': response.status_code,
            'body': json.dumps(f"Failed to retrieve data: {response.status_code}")
        }
