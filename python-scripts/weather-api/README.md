
weather.py
============================================================================= 
An AWS lambda fonction for getting weather information from internet

Author : Vincent DAGOURY
Date : 2017-04-27

# Description :

This lambda will grab weather report from api.openweathermap.org for a location name.BaseException.BaseException
It will save the content of the response in DynamoDB and will serve back this data from DynamoDB if someone request it again
The purpose of this lambda is to be assembled with API Gateway.
This lambda has been first writen durint TIAD Camp organized by D2Si on 2017/04/27 in Paris

The program fonctions as follow : 
- works on python 2.7 only
- the main function is lambda_handler
- a 'main' function exists for local tests
- it uses logging and traceback

The program will : 
- get the 'q' parameter from the RequestParameters send by API Gateway for location
- get table from DynamoDB, and if the table does not exist, it creates it
- verify that the location has been save
- if it's get the corresponding record and send it back to the API Gateway response format
- if it's not it calls the Open Weather API (from the net) and stores the resilt in DynamoDB and return back the data


Enjoy !

## Warning
Please use your own API key from api.openweathermap.org first !!

## TODO :
- Safely fail in case of timeout from OpenWeatherAPI or DynamoDB
- Externalize OpenWeatherMap.org API KEY
- maps every float to Decimal since DynamoDB does not safe float but Decimal type
- customize so the function will be the shortest possible

# Develop with DynamodDB locally (yes it's possible !)
## Prepare your DynamoDB instance locally

- Download & install DynamoDB locally
    
    > You need Java to be installed
    You'll find how to install DynamodDB here : [http://docs.aws.amazon.com/fr_fr/amazondynamodb/latest/developerguide/DynamoDBLocal.html](http://docs.aws.amazon.com/fr_fr/amazondynamodb/latest/developerguide/DynamoDBLocal.html)

- Launch DynamoDB locally

1. Prepare a logging file log4j.properties
```
$ echo "
log4j.rootLogger=DEBUG, stdout
log4j.appender.stdout=org.apache.log4j.ConsoleAppender 
log4j.appender.stdout.layout=org.apache.log4j.PatternLayout
log4j.appender.stdout.layout.ConversionPattern=LOG%d %p [%c] - %m%n
" > log4j.properties
```

2. Open a terminal on the side and launch DynamoDB

You need to reside in the local DynamoDb directory where you have unzip the installation zip file

```
java -Djava.library.path=./DynamoDBLocal_lib -jar DynamoDBLocal.jar -sharedDb -port 8000
```

- Create "weather" table (the script will create the table automatically)
```
aws dynamodb create-table \
--endpoint-url http://localhost:8000 \
--table-name weather \
--attribute-definitions AttributeName=location,AttributeType=S \
--key-schema AttributeName=location,KeyType=HASH \
--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 
```

- List local tables

```
aws dynamodb list-tables --endpoint-url http://localhost:8000
```

- Dump content of "weather" table
```
aws dynamodb scan --table-name "weather" --endpoint-url http://localhost:8000
```

- Get one item from "weather" table for one specific key
```
aws dynamodb get-item --table-name "weather" --endpoint-url http://localhost:8000 --key '{"location":{"S":"Paris"}}'
```

- Delete table
```
aws dynamodb delete-table --table-name "weather" --endpoint-url http://localhost:8000
```