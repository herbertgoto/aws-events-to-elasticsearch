#!/bin/env python

import json
import logging
import os
import string
import sys
import time
import boto3                                
import datetime

"""
Read events from SQS DLQ and stores them in S3.

Required environment variables:
SNS_TOPIC_ARN_ALERT: The topic to send exceptions.   

S3 target environment variables:
BUCKET_NAME: The name of the bucket. 
BUCKET_PATH: The path of the bucket. 

"""


s3_client = None                        # S3 client - used as target                                             
sns_client = boto3.client('sns')        # SNS client - for exception alerting purposes
                                  
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def load_data_s3(filename):
    """Load data into S3."""
    
    global s3_client

    if s3_client is None:
        logger.debug('Creating new S3 client.')
        s3_client = boto3.client('s3')  

    try:
        logger.debug('Loading batch to S3.')
        response = s3_client.upload_file('/tmp/'+filename, os.environ['BUCKET_NAME'], str(os.environ['BUCKET_PATH']) 
            + '/' + filename)

    except Exception as ex:
        logger.error('Exception in loading data to s3 message: {}'.format(ex))
        send_sns_alert(str(ex))
        raise


def send_sns_alert(message):
    """send an SNS alert"""
    try:
        logger.debug('Sending SNS alert.')
        response = sns_client.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN_ALERT'],
            Message=message,
            Subject='DLQ processing Alarm',
            MessageStructure='default'
        )
    except Exception as ex:
        logger.error('Exception in publishing alert to SNS: {}'.format(ex))
        send_sns_alert(str(ex))
        raise


def lambda_handler(event, context):
    """Read any new events from DocumentDB and apply them to an streaming/datastore endpoint."""
    
    filename = None
    fobj = None

    try:
        
        filename = 'dlq' + '-' + datetime.datetime.now().strftime("%s")
        fobj = open('/tmp/'+filename, 'w')
        logger.debug('S3 client set up.')

        for record in event['Records']:
            fobj.write(json.dumps(record['body']))
            fobj.write("\n")
                      
    except Exception as ex:
        logger.error('Exception in executing ingestion to S3: {}'.format(ex))
        send_sns_alert(str(ex))
        raise

    else:
        
        #Saves file to S3
        fobj.close()
        load_data_s3(filename)

        return {
            'statusCode': 200,
            'body': json.dumps('Success!')
        }

    finally:

        # S3 - close temp object
        fobj.close()