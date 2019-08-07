import boto3
import botocore
import os

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    old = ''
    try:
        s3.Object('Bucket名', 'test.txt').download_file('/tmp/test.txt')
        fp = open('/tmp/test.txt', 'r')
        old = fp.read()
        fp.close()
        print('old: ' + old)
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == '404':
            print('新規作成なのでスルーする')
        else:
            print('ClientError内のその他エラー')
            raise Exception(e)
    except Exception as e:
        print('その他エラー')
        raise Exception(e)
    
    fp = open('/tmp/test.txt', 'w')
    fp.write(old + ' update ')
    fp.close()
    
    s3.meta.client.upload_file('/tmp/test.txt', 'Bucket名', 'test.txt')
    os.remove('/tmp/test.txt')
