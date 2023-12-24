# sudo pip install boto3==1.0.0 を実行し、ライブラリをインストールしておく
# sudo pip install awscli を実行し、S3への接続に必要な設定をできるようにする    

# aws configure
# AWS Access Key ID: xxxxxxxxxxxxxxxxx
# AWS Secret Access Key: xxxxxxxxxxxxxxxxx
# Default region name: ap-northeast-1
# Default output format: によって設定をする

import boto3
import glob

def send_image_to_s3(bucket_name: str, files: list[str]):
    s3 = boto3.resource('s3')
    # dynamo = boto3.resource('dynamodb') dynamodbの場合はこのように指定
    bucket = s3.Bucket(bucket_name)
    for file in files:
        bucket.upload_file(file, file)

def main():
    files = glob.glob("./*.png")
    send_image_to_s3('mount-rs', files)


if __name__ == "__main__":
    main()
