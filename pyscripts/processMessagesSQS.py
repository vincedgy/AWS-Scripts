#!/usr/local/bin/python3
""" Process Messages """
import boto3
import time

def printPoint():
    print('.', end='', flush=True)

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='VDY_SQS_2')

# Process messages by printing out body and optional author name
count = 0
try:
    print ('Start processing.\n')
    print ('#;BODY;OriTime;TimeSpent')
    while True:
        # Wait 1""
        # time.sleep(1)
        # printPoint()
        for message in queue.receive_messages(MessageAttributeNames=['Author']):
            # count
            count += 1
            # Get the custom author message attribute if it was set
            if message.message_attributes is not None:
                message_time = message.message_attributes.get('Author').get('StringValue')
                float_time = float(message_time)
                current_time = time.time()
                diff = current_time - float_time
                if diff:
                    time_text = ' ({0})'.format(message_time)
            # Print out the body and author (if set)
            print('#{0};[{1}];{2};{3}s'.format(count, message.body, time_text,round(diff,2)))
            # Let the queue know that the message is processed
            message.delete()
except KeyboardInterrupt:
    print ('\nProcessing interrupted!')