#!/usr/local/bin/python3
import boto3

# Get the service resource
sqs = boto3.resource('sqs')

# Create the queue. This returns an SQS.Queue instance
queue = sqs.create_queue(QueueName='VDY_SQS_2', Attributes={'DelaySeconds': '0'})

# You can now access identifiers and attributes
print(queue.url)
print(queue.attributes.get('DelaySeconds'))