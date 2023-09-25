"""
This module contains a Lambda function that responds to S3 events.
When a new folder (dataset) is added to a specific S3 bucket and prefix,
the Lambda function triggers a Glue job with the details of the newly added dataset.

Expected S3 path format:
   <bucket>/raw/dataset_#/...
"""
import boto3
import os

GLUE_JOB_NAME = os.environ['GLUE_JOB_NAME']


def lambda_handler(event, context):
    """
    AWS Lambda function handler. Triggered by an S3 event when a new folder (dataset) is added.

    :param event: AWS Lambda uses this parameter to pass in event data to the handler.
    :param context: AWS Lambda uses this parameter to provide runtime information to your handler.
    :return: A response dict with statusCode and body.
    """

    # Extract bucket name and S3 key from the event
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    s3_key = event['Records'][0]['s3']['object']['key']

    # Extract dataset_id from the S3 key which was added recently
    parts = s3_key.split('/')
    dataset_id = parts[2] if len(parts) > 2 else None

    if not dataset_id:
        print("Could not extract dataset_id from the S3 key:", s3_key)
        return

    # Now, trigger the Glue job
    glue = boto3.client('glue')

    response = glue.start_job_run(
        JobName=GLUE_JOB_NAME,
        Arguments={
            '--bucket_name': bucket_name,
            '--dataset_id': dataset_id
        }
    )

    print(f"Started Glue job: {GLUE_JOB_NAME} with runId: {response['JobRunId']}")

    return {
        'statusCode': 200,
        'body': f"Triggered Glue job with dataset: {dataset_id}"
    }
