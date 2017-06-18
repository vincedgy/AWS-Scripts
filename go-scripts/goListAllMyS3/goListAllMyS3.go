package main

/*
-----------------
Author : Vincent DAGOURY
Date : 2017-05-03

goListAllMyS3.go
==============================================================================

# Description :
Will list all your S3 objects on all regions in one command with this Golang v1.8 program

Enjoy !

# Install go for your system
Please check [https://golang.org/doc/install](https://golang.org/doc/install)

# Install AWS SDK for Go
go get -u github.com/aws/aws-sdk-go/...

# Build the executable
go build goListAllMyS3.go

-----------------
*/
import (
	"fmt"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/ec2"
	"github.com/aws/aws-sdk-go/service/s3"
)

func main() {
	// Open session
	sess := session.Must(session.NewSession())

	// List each available regions of the current account (we need a first region)
	ec2client := ec2.New(sess, &aws.Config{Region: aws.String("eu-west-1")})
	regions, err := ec2client.DescribeRegions(&ec2.DescribeRegionsInput{})
	if err != nil {
		panic(err)
	}

	// see https://godoc.org/github.com/aws/aws-sdk-go/service/ec2#Region
	for _, region := range regions.Regions {
		fmt.Println("Region Name : ", *region.RegionName)
		//fmt.Println("Region Endpoint : ", *region.Endpoint)

		// Open S3 service for the specified region
		svc := s3.New(sess, &aws.Config{Region: aws.String(*region.RegionName)})

		// List Buckets
		var buckets *s3.ListBucketsInput
		respBuckets, err := svc.ListBuckets(buckets)
		if err != nil {
			fmt.Println(err.Error())
			return
		}

		// Run through Buckets
		for _, keyBuckets := range respBuckets.Buckets {
			// List Objects
			params := &s3.ListObjectsInput{Bucket: aws.String(*keyBuckets.Name)}
			resp, _ := svc.ListObjects(params)
			// Run through each keys
			for _, key := range resp.Contents {
				// Print out
				fmt.Println("[" + *region.RegionName + "] s3://" + *keyBuckets.Name + "/" + *key.Key)
			}
		}

	}

}
