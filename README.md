# README #

### Cooking ingredients? ###
- Python Flask, Flask RestPlus
- Serverless Framework
- AWS Lambda, AWS DynamoDB
- Swagger 2.0


### What is this repository for? ###

* 2018-04-18 Forum

### How do I get set up & running? ###

* Prerequisites: 
```
node, npm, python3, pip3, virtualenv
```
* Install Serverless & dependencies:
```
npm install serverless -g
```
* Install:
```
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
```
# Test flask app
sls wsgi serve

# Test off line Aws lambda and gateway
sls offline
```
* Deploy to AWS:
```
# Deploy all
sls deploy

# Deploy one
sls deploy function -f myFuncName

# Tail log
sls logs -f myFuncName -t
```

* Remove stack:
```
sls remove
```

### References

* https://serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb/

### Todos:

* CI/CD using CodePipeline & CodeBuild
* Deploy to kubernetes cluster (OpenWhisk/Kubeless)
* Add unit tests
* Refactor app structure using blueprint