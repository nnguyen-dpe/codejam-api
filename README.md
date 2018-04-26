# THE BUG SPIKERS
[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

## What is this repository for? 

* 2018-04-18 Forum

## Cooking ingredients? 
- Python Flask, Flask RestPlus
- Serverless Framework
- AWS Lambda, AWS DynamoDB
- Swagger 2.0

## How do I get set up & running? 

* Prerequisites: 
```sh
node, npm, python3, pip3, virtualenv
```
* Install Serverless & dependencies:
```sh
npm install serverless -g
```
* Install:
```sh
git clone git@dpe.bitbucket.org:thebugspikers/codejam-api.git
cd codejam-api

npm init -f
npm install --save-dev serverless-wsgi serverless-python-requirements serverless-dynamodb-local serverless-offline

virtualenv venv --python=python3
source venv/bin/activate

pip install flask
pip install boto3
pip install flask-restplus
pip freeze > requirements.txt
```
* Test locally:
```sh
# Test flask app
source venv/bin/activate
sls wsgi serve

# Test off line Aws lambda and gateway
sls offline
```
* Deploy to AWS:
```sh
# Deploy all
sls deploy

# Deploy one
sls deploy function -f myFuncName

# Tail log
sls logs -f myFuncName -t
```

* Remove stack:
```sh
sls remove
```

## References

* https://serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb/

## Todos:

* CI/CD using CodePipeline & CodeBuild
* Deploy to kubernetes cluster (OpenWhisk/Kubeless)
* Add unit tests
* Refactor app structure using blueprint