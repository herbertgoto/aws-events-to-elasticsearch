#!/bin/env python

import json
import logging
import os
import string
import sys
import time
import boto3                                             
from elasticsearch import Elasticsearch   
import urllib.request  


"""
Read AWS events from EventBridge and ingest them into Elasticsearch.

Required environment variables:
SNS_TOPIC_ARN_ALERT: The topic to send exceptions.   

ElasticSearch target environment variables:
ELASTICSEARCH_URI: The URI of the Elasticsearch domain where data should be streamed.

"""
                          
es_client = None                        # ElasticSearch client - used as target                                         
sns_client = boto3.client('sns')        # SNS client - for exception alerting purposes
                                  
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_es_client():
    """Return an Elasticsearch client."""
    
    global es_client
    
    if es_client is None:
        logger.debug('Creating Elasticsearch client Amazon root CA')
        """
            Important:
            Use the following method if you Lambda has access to the Internet, 
            otherwise include the certificate within the package. 

            Comment following line if certificate is loaded it as part of the function. 
        """
        get_es_certificate()                                 

        try:
            es_uri = os.environ['ELASTICSEARCH_URI']
            es_client = Elasticsearch([es_uri],
                                      use_ssl=True,
                                      ca_certs='/tmp/AmazonRootCA1.pem')
        except Exception as ex:
            logger.error('Failed to create new Elasticsearch client: {}'.format(ex))
            send_sns_alert(str(ex))
            raise

    return es_client


def get_es_certificate():                           
    """Gets the certificate to connect to ES."""
    try:
        logger.debug('Getting Amazon Root CA certificate.')
        url = 'https://www.amazontrust.com/repository/AmazonRootCA1.pem'
        urllib.request.urlretrieve(url, '/tmp/AmazonRootCA1.pem')
    except Exception as ex:
        logger.error('Failed to download certificate to connect to ES: {}'.format(ex))
        send_sns_alert(str(ex))
        raise


def send_sns_alert(message):
    """send an SNS alert"""
    try:
        logger.debug('Sending SNS alert.')
        response = sns_client.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN_ALERT'],
            Message=message,
            Subject='EventBridge to Elasticseach Alarm',
            MessageStructure='default'
        )
    except Exception as ex:
        logger.error('Exception in publishing alert to SNS: {}'.format(ex))
        send_sns_alert(str(ex))
        raise


def lambda_handler(event, context):
    """Read AWS events from EventBridge and ingest them into Elasticsearch."""
    
    try:
        # Create ES client
        es_client = get_es_client()
        logger.debug('ES client set up.')

        # Publish event to ES 
        es_client.index(index=event['source'],id=event['id'],body=json.dumps(event))     

    except Exception as ex:
        logger.error('Exception in executing ingestion: {}'.format(ex))
        send_sns_alert(str(ex))
        raise

    else:
        
        return {
            'statusCode': 200,
            'body': json.dumps('Success!')
        }