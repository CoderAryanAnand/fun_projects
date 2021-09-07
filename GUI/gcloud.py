# Imports the Google Cloud client library
from google.cloud import storage

# Instantiates a client
storage_client = storage.Client(client_info='gcloud-key.json')

# The name for the new bucket
bucket_name = "passwords"

# Creates the new bucket
bucket = storage_client.create_bucket(bucket_name)

print("Bucket {} created.".format(bucket.name))
