def do(event, context):
    print(event['headers'])

    return {
        "statusCode": 200
    }