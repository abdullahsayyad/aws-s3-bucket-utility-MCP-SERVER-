import aioboto3
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()





class S3ServiceClient:
    def __init__(self):
        self.session = aioboto3.Session()
        
        # Check if specific buckets are set in the .env file
        self.specified_buckets = os.getenv("S3_BUCKETS")

        # If bucket names are provided, split them into a list
        if self.specified_buckets:
            self.specified_buckets = self.specified_buckets.split(",")
        else:
            # If no specific buckets are set, allow access to all
            self.specified_buckets = None

    async def getAllBucketData(self):
        # If we have specific buckets set, just return them
        if self.specified_buckets:
            return self.specified_buckets
        
        # Otherwise, fetch all available buckets from S3
        async with self.session.client('s3') as s3_client:
            try:
                response = await s3_client.list_buckets()
                return [bucket["Name"] for bucket in response.get('Buckets', [])]
            except Exception as error:
                return f"Failed due to: {error}"




    async def getAllBucketObjects(self, region=None):
        # Get the list of buckets (either specified or all)
        allBuckets = await self.getAllBucketData()
        bucketObjects = {}

        async with self.session.client('s3') as s3_client:
            for bucket_name in allBuckets:
                try:
                    params = {"Bucket": bucket_name}

                    # If a region is specified, add it to the request
                    if region:
                        params["region_name"] = region

                    response = await s3_client.list_objects_v2(**params)

                    # If the bucket has files, store their names
                    if "Contents" in response:
                        objects = [obj["Key"] for obj in response["Contents"]]
                        bucketObjects[bucket_name] = objects
                    else:
                        bucketObjects[bucket_name] = f"No objects found in {bucket_name}."
                except Exception as e:
                    bucketObjects[bucket_name] = f"Failed to load objects due to: {e}"

        return bucketObjects




    async def getCsvObjects(self):
        # Get all buckets first
        allBuckets = await self.getAllBucketData()
        csvObjects = {}

        async with self.session.client('s3') as s3_client:
            for bucket_name in allBuckets:
                try:
                    response = await s3_client.list_objects_v2(Bucket=bucket_name)

                    # Filter out only CSV files
                    if "Contents" in response:
                        csv_files = [obj["Key"] for obj in response["Contents"] if obj["Key"].endswith(".csv")]

                        # If there are CSV files, store them; otherwise, say none were found
                        csvObjects[bucket_name] = csv_files if csv_files else "No CSV files found."

                except Exception as e:
                    csvObjects[bucket_name] = f"Failed to retrieve CSVs: {e}"

        return csvObjects




    async def readCsvFile(self, bucket_name, file_key):
        # Read a specific CSV file from S3
        async with self.session.client('s3') as s3_client:
            try:
                response = await s3_client.get_object(Bucket=bucket_name, Key=file_key)

                # Read the file's contents as a stream
                async with response["Body"] as stream:
                    csv_content = await stream.read()
                    return csv_content.decode("utf-8")
                
            except Exception as e:
                return f"Failed to read {file_key} in {bucket_name}: {e}"
