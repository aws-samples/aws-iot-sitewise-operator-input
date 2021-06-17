# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
from decimal import Decimal
import json
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
tableName = 'operator-input'
table = dynamodb.Table(tableName)

#Write data into DynamoDB
def put_operator_input(timestamp, alias, value, comment):
    item = {
            'timestamp': timestamp,
            'propertyAlias': alias,
            'propertyValue': value,
            'comment': comment
    }
    try:
        response = table.put_item(Item=item)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response

#Read last status from DynamoDB
def read_last_operator_input(alias):
    try:
        response = table.query(
            KeyConditionExpression=Key('propertyAlias').eq(alias),
            ScanIndexForward=False, 
            Limit=1
        )
        print(response)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return response

def lambda_handler(event, context):
    print("event: {}".format(event))
    response_code = 405
    response_body = {}
    method = event['httpMethod']
    path = event['path']
    alias = '/' + path.split("/", 2)[2]
    
    if method=='POST':
        body = json.loads(event['body'], parse_float=Decimal)
        print(body)
        response = put_operator_input(body['timestamp'], alias, body['value'], body['comment'])
        print(response)
        response_code = response['ResponseMetadata']['HTTPStatusCode']
        response_body=json.dumps('OK!')
    elif method=='GET':
        response = read_last_operator_input(alias)
        print (response)
        response_code = response_code = response['ResponseMetadata']['HTTPStatusCode']
        if (response_code == 200):
            if (response['Count']>0) :
                resp = {
                    'alias':response['Items'][0]['propertyAlias'],
                    'timestamp': int(response['Items'][0]['timestamp']),
                    'value':float(response['Items'][0]['propertyValue'])
                }
            else : 
                resp = {}
            response_body = json.dumps(resp)
    
    
    resp = {
        'statusCode': response_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            },
        'body': response_body
    }
    print (resp)
    return resp
