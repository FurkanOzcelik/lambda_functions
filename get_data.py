import boto3
from boto3.dynamodb.conditions import Attr


def sa(category):
    client = boto3.resource('dynamodb',aws_access_key_id='key', aws_secret_access_key='key', region_name='us-east-1')
    # dynamodb = boto3.resource('dynamodb')
    table = client.Table('table')
    
    response = table.scan(
        FilterExpression=Attr("cat").eq(category)
    )
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
        print(len(data))
        
    result = []
    for x in data:
        result.append(x['text'])
    return result
