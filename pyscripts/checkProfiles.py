#! /usr/bin/env python
'''
checkProfiles.py : which will test all your entries in ~/.aws/credentials
author : VinceDgy
date   : 2017-06-17
'''
import ConfigParser, os, boto3, botocore
# Read the aws credentials used by awscli, SDKs, boto etc...
config = ConfigParser.ConfigParser()
config.read([os.path.expanduser('~/.aws/credentials')])
# For each configurations in the credentials
for PROFILE in config.sections():
    # Catch the decription (if exists)
    try: 
        DESCRIPTION = config.get(PROFILE,'description')
    except:
        DESCRIPTION = '<no description>'    
    # Get Key and secret, then test on S3 
    try: 
        ACCESS_KEY = config.get(PROFILE,'aws_access_key_id')
        SECRET_KEY = config.get(PROFILE,'aws_secret_access_key')
        client = boto3.client(
            's3',
            aws_access_key_id=ACCESS_KEY,
            aws_secret_access_key=SECRET_KEY,
        )
        if ( client.list_buckets() != None ) :
            RESULT = "OK"
        else:
            RESULT = "OK but no S3 bucket"
    except botocore.exceptions.ClientError as e :
        RESULT = "KO\t" + e.response['Error']['Message']
    # Print out the result for this configuration
    print(PROFILE + "\t" + DESCRIPTION + "\t" + RESULT)

# That's it