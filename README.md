# AWS-Script

My little collection of scripts (shell, python, go, etc...) for AWS assets



SERVERLESS COMPUTING
=====================

# Local dev of lambda nodeJS based code
## aws-lambda-local
[https://www.npmjs.com/package/aws-lambda-local](https://www.npmjs.com/package/aws-lambda-local)
``npm install -g aws-lambda-local

# Docker container for lambda local dev
[https://github.com/lambci/docker-lambda](https://github.com/lambci/docker-lambda)


# ServerLess Framework 
-----------------------

1. Install serverless globally
``npm install serverless -g

2. Create an AWS Lambda function in Node.js
``serverless create --template aws-nodejs

3. Deploy to live AWS account
``serverless deploy

4. Function deployed!
[http://api.amazon.com/users/update](http://api.amazon.com/users/update)

# Other Serverless frameworks
    * Apex, Qualys

====================================================================================
# Operational ServerLess

* APM on ServerLess : NewRelic, Datadog ?
AWS CloudWatch -> monitores Lambda (nb d'exec/invocations, exec time/duration)
Scheduling ? or event ?
* Errors ? 
=> AWS Cloudwatch for error monitoring
1. Code Error => /!\ if lambda failed it is restarted by default
2. Execution error (out of mem, out of exec time)
3. Lambda runtime error
* Logs
- LogGroup, LogStream (a lot of logs by default just for Lambda engine itself)
==> Another logging system is mandatory
4. Tracing (where my code spends to much time) : APM : AppDynamics
-> We want to know where Lambda spends the most of its time
- AWS X-Ray (preview on April 19th)

# Challenges with Serverless Architecture

1. Never ending looping (on S3) 
2. Streaming from Kinesis (like a managed Kafka) : infinite processing on 1 stream event
3. Latency ??
- <10ms most of the time
- What if one lambda is a sequence = is it bigger then a simple but more complex code ?
- It it fast enough (HPC London Paris) : networking 4-6 ms
- Redis < 10us
- CPU addition < 10ns 
- billing is per 100ms
4. Warms-up time
AWS startup a container for its code execution, mount network interface etc...
- Very slow on first exec (100d of sec) !!
- Reschedule costs a lot ()
- What about new version of code ? Again, latency

# Lambda
-> To be well knowed on behaviour

/!\ drawbacks on Event source behaviour / configuration
- One event at a time 
- Retries on batching event (like DynamoDB or SQS)
- Dead letter queues could be crucial for messaging application

Limits &nd throtting :
- Lambda is limited to 100 currencrent executions
- 1000 invocations/s max by default
- AWS provides no metrics
- Look throtting
- estimate concurrency based on function duration number of calls

# Understanding new services
## Other managed services : 
- no RDS for Lamba
- Prefere SQS/Kinesis (not RabbitMQ)

New services -> new experties
- DynamoDB : talve/index, read/write capacity estimation, optimize perf/cost
- Kinesis : sharding for multiplexing and scalability, when to reshard/merge shards ?

Scalability : 
- Scaling up/down needs to be automated
- not always simple (moving bd is at a cost event for DynamoDB)

# Continuus Delivery

## Testing is not ready : 
- How do I replicate Lambda in my CI environnement ? (with S3, DynamoDB etc...)
- Will I use AWS services for UnitTesting
- What about mocking

## Local deployement to iterate fast ?
- Replicate Lambda locally : yes with the help of docker (see above) and DynamoDB locally installed
- How can I simulate AWS Services
- "localstack" can simulate locally AWS Stack, but it's very young

## Packaging and versioning ?
- Managing verdioning : easy for the code, Lambda itself can be versioned in AWS
- Deploying the same version accross environnement ? 
    Is there a deployement artifact I can share accross environement and accross accounts (Prod/Staging)

## Most frameworks are designed to push from local machine
- Build the code, get dependencies, push
- Can be duplicated on CI
- But not realy artifact I can share/deploy

## What is an application ?

### Is it a function ?
- Deployed independently
- Versioned independently
> What about shared libraries between functions

### Is in all my functions
- Versioned as a whole ? 
- With bundled shared libraries
- Same artifcat with different
- Deployed together or independently
> Functions and dependencies can sum up to a big artifact (megabytes)
>> The answer is probably somewhere in the middle

## ServerLess is the future
- Focus on Business logic that actually matters
- Much simpler apps
- Billing warning !!

Serverless creates many new challenges
- How can we adapt standard code best practices
- How do operate these new apps ?

## From NOps to New Ops
- No longer sysadmins or netadmins
- Supervision remains simimar but requires new tools
- aA big focus on new architectures and new backends

--------------------------------------------------------------------------------------------------------------

# ServerLess Analytics (Adways)

Presenter : Audric Guidon
Resp. Back Office, Solutions Architect at Adways
Adways -> Leader interactive video, international, eLearning, Adv

Use case : Needs to get information on interactions usage and figures.

Analytics needs to be very scalable (short term analysis from.
More than 1 million of interaction /day

New solution :
Serverless most of the time as possible, mainly for resilience and for the pay as you go model.

## Actual stack
Beanstalk, S3, EMR, Redshift (high performance, scalable)

2 * ds2.xlarge = 4To = 1275 €
+ EMR toutes les 6h = 100 €
+ beanstalk (php) Load balancé = 100 €
Cout fixe de 1475 €
+ preprod = 2k€/month

What about Athena : 
querying with SQL on S3 files with format csv, json, column (orcq, parkay). But not an alternative before RedShift but ok for BI queries (simple, per execution), 5$/To.
* /!\ 5 concurrent queries MAX
* needs to partition, important for performance and time spent reduction
* Columns format

## Solution "Serverless"
    - API Gateway : only for excecptionnal use, because too expensive vs CloudFront BeanStalk
    - Firehose (64Mo MAX because of Lambda) -> S3 objects (formated)
    - Lambda (process 64Mo per file max) --> S3 buckets
    - Athena + QuickSight (like Kibana, very powerfull) only for BI users (not customers)
    - Athena + ApiGateway (not much volume, ++security) + Lambda (Java SDK) : for customers

5x less expensive
CloudFront/Beanstalk/S3 cost

/!\ Athena in Virginia only -> cost a lot because without Ireland

--------------------------------------------------------------------------------------------------------------

# Serverless made in Google
Guillaume Laforge - Developer advocate sur Google Cloud

## Chatbots with API.AI & Google Cloud Functions
Google Cloud Functions
API.AI bought by Google in Sept 2016

Intro : IRC is not dead, XChat

Game changer : Speach to text with ML-powered voice recognition. 
Deep learning, neuron networks, voice recognition algorithmics

At google : ML-driven Natural Language Processing

