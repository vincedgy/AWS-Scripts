#! /usr/bin/env python
"""
weather.py : An AWS lambda fonction for getting weather information from internet
Author : Vincent DAGOURY
Date : 2017-04-27
Description :
This lambda will grab weather report from api.openweathermap.org for a location name.BaseException.BaseException
It will save the content of the response in DynamoDB and will serve back this data from DynamoDB if someone request it again
The purpose of this lambda is to be assembled with API Gateway.BaseException
This lambda has been first writen durint TIAD Camp organized by D2Si on 2017/04/27 in Paris
Enjoy !

Warning : Please use your own API key from api.openweathermap.org first !!

TODO :
- Safely fail in case of timeout
- Externalize OpenWeatherMap.org API KEY
"""
from __future__ import print_function  # Python 2/3 compatibility
import urllib
import urllib2
import traceback
import json
import logging
import sys

import boto3
from botocore.exceptions import ClientError

# Define decimal precision
from decimal import *
getcontext().prec = 3

LOGGING_LEVEL = 'INFO'
#logging.basicConfig(
#    level = getattr(logging, LOGGING_LEVEL),
#    format = '%(asctime)s \033[0;34m%(name)-12s \033[0;33m%(levelname)-8s \033[0;37m%(message)s\033[0m',
#    datefmt = '\033[0;31m%m/%d/%Y %I:%M:%S %p\033[0m'
#)
logging.basicConfig(
    level = getattr(logging, LOGGING_LEVEL),
    format = '%(asctime)s %(name)-8s %(levelname)-8s %(message)s',
    datefmt = '%Y-%m-%d %I:%M:%S %p'
)

## automate http://api.openweathermap.org/data/2.5/forecast?id=524901&APPID=eb6397a6776974b07c1abc35f64af1a2
API_URL = 'http://api.openweathermap.org/data/2.5/forecast'
API_KEY = 'eb6397a6776974b07c1abc35f64af1a2'
TABLE_NAME = 'weather'

REQUEST_HEADERS = {
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
"Accept": "application/json",
}

# Globals
## _dynamodb = boto3.resource("dynamodb", region_name='eu-west-1')    
_dynamodb = boto3.resource('dynamodb', region_name='eu-west-1', endpoint_url='http://localhost:8000')

## Uncomment If you use DynDb localy for testing
def getTable(dynamodb, tablename):
    try:
        table = dynamodb.Table(tablename)
        logging.info('Table ' + tablename + ' exists since ' + str(table.creation_date_time))
        return table
    except ClientError as e:
        if e.response['Error']['Code'] == u'ResourceNotFoundException':
            logging.error('Table ' + tablename + ' needs to be created.')
            try:
                table = dynamodb.create_table(
                    TableName=tablename,
                    KeySchema=[{'AttributeName': 'location', 'KeyType': 'HASH'}],
                    AttributeDefinitions=[{'AttributeName': 'location', 'AttributeType': 'S'}],
                    ProvisionedThroughput={'ReadCapacityUnits': 1, 'WriteCapacityUnits': 1}
                    )
                return table
            except ClientError:
                traceback.print_exc()
                sys.exit(1)

# =============================================================================
def get_weather(table, q):
    """xxx"""
    data = {}
    try:
        response = table.get_item(Key={'location':q})
        if response['Item'] is not None:
            data = response['Item']
        #print(json.dumps(data, indent=4))
    except KeyError:
        logging.info("No data found in DynDB")
    except ClientError as e:
        logging.error(repr(traceback.format_stack(),e))
    finally:
        return data

# =============================================================================
def mapData(data, q):
    try:
        # The whole item to send back
        myItem = {}
        # Handle Weather information
        weatherList=[]
        for a in data['list']:
            # Handle Subweather information
            subweatherList=[]
            for b in a['weather']:
                subweather = {
                    'main' : b['main'],
                    'id' : b['id'],
                    'icon' : b['icon'],
                    'description' : b['description']
                }
                subweatherList.append(subweather)
            # Build list item to be added to weatherList
            weather = {
                'clouds' : {
                    'all' : a['clouds']['all']
                },
                #'rain' : repr(a['rain']),
                #'snow' : repr(a['snow']),
                #'sys' : repr(a['sys']),
                'dt_txt' : a['dt_txt'],
                'dt' : a['dt'],
                'wind' : {
                    'speed' : Decimal(repr(a['wind']['speed'])),
                    'deg' : Decimal(repr(a['wind']['deg']))
                },
                'weather' : subweatherList,
                'main' : {
                    'temp_kf' : Decimal(repr(a['main']['temp_kf'])),
                    'temp' : Decimal(repr(a['main']['temp'])),
                    'grnd_level' : Decimal(repr(a['main']['grnd_level'])),
                    'temp_max' : Decimal(repr(a['main']['temp_max'])),
                    'sea_level' : Decimal(repr(a['main']['sea_level'])),
                    'humidity' : a['main']['humidity'],
                    'pressure' : Decimal(repr(a['main']['pressure'])),
                    'temp_min' : Decimal(repr(a['main']['temp_min']))
                }
            }
            # rain field
            if len(a['rain']) > 0:
                weather['rain'] = { '3h': Decimal(repr(a['rain']['3h'])) }
            # snow field
            try:
                weather['snow'] = { '3h': Decimal(repr(a['snow']['3h'])) }
            except:
                pass
            #
            weatherList.append(weather)
        myItem = {
            'location' : q,
            'cod' : data['cod'],
            'cnt' : data['cnt'],
            'city' : {
                'country' : data['city']['country'],
                'id' : data['city']['id'],
                'coord' : {
                    'lat' : Decimal(repr(data['city']['coord']['lat'])),
                    'lon' : Decimal(repr(data['city']['coord']['lon']))
                }
            },
            'list': weatherList
        }
        
    except (Exception, ClientError) as error:
            logging.error(error)
    finally:
        return myItem

# =============================================================================
def save_weather_data(table, q, data):
    """xxx"""
    try:
        if not (q is None or data is None):
            response = table.put_item(Item = mapData(data,q))
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                logging.info("PutItem succeeded:")
    except (Exception, ClientError) as error:
        logging.error(error)
    finally:
        return data

# =============================================================================
def lambda_handler(event, context):
    """xxx"""
    # params represent the Query parameters sent to the API
    params = {}
    params['q'] = event['queryStringParameters']['q']
    params['APPID'] = API_KEY
    # Test if location is stored in DynamoDB
    logging.info('Looking for weather info for location ' + params['q'] + ' from DynDb.')
    table = getTable(_dynamodb, TABLE_NAME)
    data = get_weather(table, params['q'])
    content = ''
    # If it's not, we ask for the weather service
    if data is None or len(data) == 0:
        logging.info('No data -> Getting weather for location ' + params['q'] + ' from the Web.')
        url_values = urllib.urlencode(params)
        full_url = API_URL + '?' + url_values
        request = urllib2.Request(full_url, headers=REQUEST_HEADERS)
        response = urllib2.urlopen(request)
        content = response.read()
        data = json.loads(content)
        if content is not None and len(content) > 1:
            logging.info('Saving data for location ' + params['q'] + ' to DynDb.')
            save_weather_data(table, params['q'], data)
        else:
            logging.info('No data found for location ' + + params['q'])
    logging.info('Returning result (even if it''s empty) and ending.')
    return {
        "statusCode": 200,
        "headers": {},
        "body": data
    }

# =============================================================================
if __name__ == '__main__':
    logging.info('Starting main function (for testing...')
    EVENT = {'queryStringParameters':{'q':'Paris'}}
    CONTEXT = ''
    logging.info(lambda_handler(EVENT, CONTEXT))
