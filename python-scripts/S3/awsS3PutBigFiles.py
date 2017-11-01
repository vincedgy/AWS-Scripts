""" """
# Create a big file (100 Mb): 
# dd if=/dev/zero of=/tmp/bigfile bs=1024 count=0 seek=$[1024*100]
import os
import sys
import threading
import boto3
from boto3.s3 import transfer 

class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (
                    self._filename, 
                    self._seen_so_far, 
                    self._size,
                    percentage))
            sys.stdout.flush()  

# ---------------------------------------------------------------------
# Main
if __name__ == '__main__':
    client = boto3.client('s3', 'eu-west-1')
    config = transfer.TransferConfig(
        multipart_threshold=8 * 1024 * 1024,
        max_concurrency=10,
        num_download_attempts=10,
    )

    uploading = transfer.S3Transfer(client, config)
    uploading.upload_file(
        '/tmp/bigfile',
        'e-attestations-ova',
        'bigfile',
        callback=ProgressPercentage('/tmp/bigfile')
        )

