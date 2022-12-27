import boto3
from boto3.dynamodb.conditions import Attr


def sa(category):
    client = boto3.resource('dynamodb',aws_access_key_id='AKIAQUFZQ62BJDT37NQ3', aws_secret_access_key='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', region_name='us-east-1')
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
