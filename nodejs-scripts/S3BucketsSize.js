'use strict';
var async = require('async');
var AWS = require('aws-sdk');

var s3 = new AWS.S3({ apiVersion: '2006-03-01' });

var credentials = new AWS.SharedIniFileCredentials({
    profile: 'default'
});
AWS.config.credentials = credentials;

s3.listBuckets({}, function (err, data) {
    if (err) console.error(err, err.stack); // an error occurred
    else {
        data.Buckets.forEach(function (Bucket) {
            s3.getBucketLocation({ Bucket: Bucket.Name }, function (err, data) {
                if (err) console.error(err, err.stack); // an error occurred
                else {
                    s3.listObjects({ Bucket: Bucket.Name }, function (err, data) {
                        if (err) console.error(err, err.stack); // an error occurred
                        else {
                            var TotalSize = 0;
                            var Objects = data.Contents;
                            Objects.forEach(function(item) {
                                TotalSize += item.Size;
                            });
                            console.log(
                                "s3://" + Bucket.Name, 
                                TotalSize + "B", 
                                Math.round(TotalSize/1024).toFixed(2).toString() + "K",
                                Math.round(TotalSize/(1024*1024)).toFixed(2).toString() + "M"
                                );
                        }
                    });
                }
            });
        });
    }
});