from mcp.server.fastmcp import FastMCP 
from s3_tools import S3ServiceClient

# Setting up FastMCP and the S3 manager
mcp = FastMCP("AWS-S3-AccessTool")
s3_manager = S3ServiceClient()

# Tool to list all available buckets
@mcp.tool()
async def getAvailableBuckets():
    try:
        return await s3_manager.getAllBucketData()
    except Exception as e:
        return f"Error: {str(e)}"
    

# Tool to list all objects in the buckets
@mcp.tool()
async def getBucketObjects():
    try:
        return await s3_manager.getAllBucketObjects()
    except Exception as e:
        return f"Error: {str(e)}"


# Tool to list only CSV files from the buckets
@mcp.tool()
async def getCsvObjects():
    try:
        return await s3_manager.getCsvObjects()
    except Exception as e:
        return f"Error: {str(e)}"


# Tool to read a specific CSV file from S3
@mcp.tool()
async def readCsvObject(bucket_name: str, file_key: str):
    try:
        return await s3_manager.readCsvFile(bucket_name, file_key)
    except Exception as e:
        return f"Error: {str(e)}"


# Running the FastMCP server if this script is executed
if __name__ == "__main__":
    mcp.run(transport='stdio')
