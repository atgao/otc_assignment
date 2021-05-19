import sys
import botocore
import boto3
from botocore.exceptions import ClientError
import json 
from datetime import datetime

def lambda_handler(event, context):
    rds = boto3.client('rds')
    lambdaFunc = boto3.client('lambda')
    print('Trying to get Environment variable')
    try:
        funcResponse = lambdaFunc.get_function_configuration(FunctionName='RDSStartFunction')
        DBinstance = funcResponse['Environment']['Variables']['DBInstanceName']
        print('Starting RDS service for DBInstance : ', DBinstance)
    except ClientError as e:
        print(e)    
    try:
       response = rds.start_db_instance(DBInstanceIdentifier=DBinstance)
       print('Success :: ') 
       now = datetime.now()
       _ = rds.add_tags_to_resource(ResourceName='arn:aws:rds:us-west-2:708133391835:db:rds-postgresql-10mintutorial',
            Tags=[{
                'Key': 'lastStartTime',
                'Value': now.strftime("%H:%M:%S")},
                ]
            )
       return json.loads(json.dumps(response, default=str))
    except ClientError as e:
        print(e)    
    return {'message' : "Script execution completed. See Cloudwatch logs for complete output"}