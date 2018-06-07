import json
import os
from urllib.parse import unquote
import boto3

def put_product__http(event, context):
    payload = json.loads(event['body'])
    product = {
        'name': unquote(event['pathParameters']['name']),
        'price': payload['price'],
        'description': payload['description']
    }
    dynamo_db = boto3.resource('dynamodb')
    table = dynamo_db.Table(name=os.getenv('PRODUCT_TABLE_NAME'))
    table.put_item(Item=product)
    print('Saved product {}'.format(product['name']))
    return {
        'statusCode': '200',
        'body': json.dumps(product),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
