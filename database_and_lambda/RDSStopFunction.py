import sys
import botocore
import boto3
import json 
from botocore.exceptions import ClientError
def lambda_handler(event, context):
    rds = boto3.client('rds')
    lambdaFunc = boto3.client('lambda')
    print('Trying to get Environment variable')
    try:
        funcResponse = lambdaFunc.get_function_configuration(FunctionName='RDSStartFunction')
        DBinstance = funcResponse['Environment']['Variables']['DBInstanceName']
        print('Stopping RDS service for DBInstance : ', DBinstance)
    except ClientError as e:
        print(e)    
    try:
       response = rds.stop_db_instance(DBInstanceIdentifier=DBinstance)
       print('Success :: ') 
       return json.loads(json.dumps(response, default=str))
    except ClientError as e:
        print(e)    
    return {'message' : "Script execution completed. See Cloudwatch logs for complete output"}