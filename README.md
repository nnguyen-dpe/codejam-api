# SERVERLESS POC
[![standard-readme compliant](https://img.shields.io/badge/standard--readme-OK-green.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

## What is this repository for? 

* Brown bag session


## Stack? 
| Tech                  |
| --------------------- |
| Python                |
| Flask, Flask RestPlus |
| Serverless Framework  |
| MongoDB               |
| Swagger 2.0           |



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
cd codejam-api && git checkout feature/openwhisk

npm init -f
npm install --save-dev serverless-wsgi serverless-python-requirements serverless-offline

virtualenv venv --python=python3
source venv/bin/activate
pip install -r requirements.txt
```

* Test & dev locally:
```sh
# Test flask app
source venv/bin/activate
sls wsgi serve -p 9001

# Run integration test
cd forum-01-developers-api/_integration-tests
./gradlew clean test


* Setup & package openwhisk environment:
```sh
# Run the following to install the dependencies and create a virtualenv using a compatible Docker image:
docker run --rm -v "$PWD:/tmp" openwhisk/python3action bash \
  -c "cd tmp && virtualenv virtualenv --python=python3 && source virtualenv/bin/activate && pip install -r requirements.txt"

```

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

* Add unit tests & mock framework
* Debugging local & live function
* CI/CD via CodePipeline & CodeBuild
* Add Auth layer
* Monitoring with IOPipe
* Package and deploy to kube/ose (OpenWhisk/Kubeless/Fission)

## Developers:

* Nam Nguyen 
* Rahul Sharma