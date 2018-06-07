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


def get_product__http(event, context):
    product_name = unquote(event['pathParameters']['name'])

    dynamo_db = boto3.resource('dynamodb')
    table = dynamo_db.Table(name=os.getenv('PRODUCT_TABLE_NAME'))
    result = table.get_item(Key={'name': product_name})

    try:
        product = result['Item']
    except KeyError:
        print('Could not find product {}'.format(product_name))
        return {
            'statusCode': '404',
            'body': 'Product not found'
        }
    print('Retrieved product {}'.format(product_name))

    return {
        'statusCode': '200',
        'body': json.dumps(
            {
                'name': product['name'],
                'price': product['price'],
                'description': product['description']
            }
        ),
        'headers': {
            'Content-Type': 'application/json'
        }
    }


def delete_product__http(event, context):
    product_name = unquote(event['pathParameters']['name'])

    dynamo_db = boto3.resource('dynamodb')
    table = dynamo_db.Table(name=os.getenv('PRODUCT_TABLE_NAME'))
    table.delete_item(Key={'name': product_name})
    print('Deleted product {}'.format(product_name))

    return {
        'statusCode': '204',
        'body': ''
    }
