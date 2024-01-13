import boto3
import json

def convert_intlist_to_byte(int_array):
    # 配列内の各要素を文字列に変換
    str_array = [str(item) for item in int_array]
    # CSV形式で文字列を連結
    csv_string = ','.join(str_array)
    # 文字列をバイト型に変換
    byte_string = csv_string.encode('utf-8')
    
    return byte_string

#needs ~/.aws/credentials

ENDPOINT_NAME = "built-in-algo-lightgbm-regression-model-2024-01-13-09-30-27-219"

def invoke_api(int_array):
    client = boto3.client('sagemaker-runtime')

    body_req = convert_intlist_to_byte(int_array)
    response = client.invoke_endpoint(
        EndpointName = ENDPOINT_NAME,
        Body = body_req,
        ContentType = 'text/csv',
        Accept = 'application/json'
    )
    body = response['Body']
    res = json.load(body)
    
    return int(res["prediction"][0])

# test invoke_api(body)
# print(convert_intlist_to_byte([1, 58, 0, 0, 146]))