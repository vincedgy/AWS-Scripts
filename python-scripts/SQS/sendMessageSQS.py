#!/usr/local/bin/python3
import boto3, time, sys

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='VDY_SQS_2')

# Handle arguments
InputMessage = '<void>'
if len(sys.argv) > 1:
    try:
        i=int(sys.argv[1])
        InputMessage=str(sys.argv[2])
    except:
        i=1
else:
    i=1

# Send as many messages needed
max=i
while (i>0):
    currentTime = str(time.time())
    message = '#' + str(max-i+1) + ':' + InputMessage
    response = queue.send_message(MessageBody=message, MessageAttributes={
        'Author': {
            'StringValue': currentTime,
            'DataType': 'String'
        }
    })
    print('Sending: \'{0}\' with ID={1}'.format(message, response.get('MessageId')))
    i -= 1