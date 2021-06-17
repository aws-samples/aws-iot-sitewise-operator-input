# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
import boto3
import json
import time
import uuid
import sys
from boto3.dynamodb.types import TypeDeserializer
from decimal import Decimal as D

def lambda_handler(event, context):
    print("event: {}".format(event))
    client = boto3.client('iot-data')
    deserializer = TypeDeserializer()
    TOPIC = "lambda/operator/input"
    
    # Extending JSONEncoder to convert Decimal()
    class DecimalEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, D):
                return float(obj)
            return json.JSONEncoder.default(self, obj)
    
    for record in event['Records']:
        print(record['eventID'])
        print(record['eventName'])
        if record['eventName'] == 'INSERT':
            newEntry = record['dynamodb']['NewImage']
            data_temp = {k: deserializer.deserialize(v) for k,v in newEntry.items()}
            data_temp["entryId"] = str(uuid.uuid4());
            data = DecimalEncoder().encode(data_temp)
            response = client.publish(
                topic=TOPIC,
                qos=1,
                payload=data
            )
            print("Response ======\n{}".format(response))
    return {
        'statusCode': 200,
        'body': json.dumps('OK!')
    }
