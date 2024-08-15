import streamlit as st
import boto3
import json
from botocore.exceptions import NoCredentialsError, ClientError

# Initialize the S3 client
s3 = boto3.client('s3')

# Define the S3 bucket name and the JSON file name
bucket_name = 'real-estate-data-bucket'
s3_file_name = 'rentcast_data.json'

# Function to load data from S3
def load_data_from_s3():
    try:
        # Fetch the JSON file from S3
        response = s3.get_object(Bucket=bucket_name, Key=s3_file_name)
        content = response['Body'].read().decode('utf-8')
        rentcast_data = json.loads(content)
        return rentcast_data
    except NoCredentialsError:
        st.error("AWS credentials not available.")
        return None
    except ClientError as e:
        st.error(f"Failed to load data from S3: {e}")
        return None

# Streamlit UI
st.title("Real Estate Investment Dashboard")

# Load the data from S3
data = load_data_from_s3()

# Display the data if available
if data:
    st.write("### Rental Market Statistics")
    st.write(f"Median Rent: ${data['medianRent']:,.2f}")
    st.write(f"Average Rent: ${data['averageRent']:,.2f}")
    st.write("### Market Listing Trends")
    st.write(f"Number of Listings: {data['numListings']}")
    st.write(f"Average Price per Square Foot: ${data['pricePerSqft']:,.2f}")
    
    # Display raw JSON data
    st.write("### Raw Data")
    st.json(data)
else:
    st.warning("No data available. Please try again later.")
