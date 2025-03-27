# AWS S3 access tool for MCP Clients 🪣⚙️





https://github.com/user-attachments/assets/976dce46-6ee3-4c1a-b5eb-8ca1575df099



The tool supports environment-based bucket selection, meaning you can restrict access to specific buckets using an .env file.

## Key Features
 - List available S3 buckets
 - Fetch objects from specific or all buckets
 - Filter and retrieve only CSV files
 - Read the content of a CSV file from S3


## Requirements
Ensure you have the following dependencies installed:

    pip install aioboto3 mcp[cli] python-dotenv

## Environment Setup

    AWS_ACCESS_KEY_ID=your_access_key
    AWS_SECRET_ACCESS_KEY=your_secret_key
    AWS_REGION=your_region
    S3_BUCKETS=bucket1,bucket2  # (Optional) List of buckets to access




## MCP Client Configuration

 

 - Configuration for  Cursor.ai

	 
        {
        "mcpServers": {
	        "AWS-S3-AccessTool": {
		        "command": "python",
		        "args": ["C:your-absolute-path-to-the-file\\main.py"]
				
				}
			}
		}


## License ⚖️
This project is open-source and available under the MIT License.
