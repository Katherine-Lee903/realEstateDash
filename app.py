import streamlit as st
import boto3
import requests
import json

# Set up S3 client
s3 = boto3.client('s3')
bucket_name = 'real-estate-data-bucket'

def load_data():
    # Fetch the latest file from S3
    objects = s3.list_objects_v2(Bucket=bucket_name)['Contents']
    latest_file = sorted(objects, key=lambda x: x['LastModified'], reverse=True)[0]
    file_name = latest_file['Key']
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    return json.load(response['Body'])

st.title('Real Estate Investment Dashboard')
st.write("This dashboard provides insights into real estate rental markets.")

# Load data
data = load_data()
st.json(data)  # Display the data as JSON

# Visualization (basic example)
st.write("### Rental Market Statistics")
st.write(f"Median Rent: {data['medianRent']}")
st.write(f"Average Rent: {data['averageRent']}")
