import boto3
import json

# Initialize a session using Amazon DynamoDB
session = boto3.session.Session()
dynamodb = session.resource('dynamodb')
s3 = session.client('s3')


def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    table_name = 'your_table_name'

    existing_tables = dynamodb.meta.client.list_tables()['TableNames']

    if table_name not in existing_tables:
        table = dynamodb.create_table(
            TableName=table_name,
            KeySchema=[
                {
                    'AttributeName': 'dataset_id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'campaign_id',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'dataset_id',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'campaign_id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )
        table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
    else:
        table = dynamodb.Table(table_name)

    s3_object = s3.get_object(Bucket=bucket, Key=key)
    s3_content = s3_object['Body'].read().decode('utf-8')

    # TODO: Adjust this part to match the actual format of your data
    items = json.loads(s3_content)

    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item={
                'dataset_id': item['dataset_id'],
                'campaign_id': item['campaign_id'],
                # ...other item attributes
            })
