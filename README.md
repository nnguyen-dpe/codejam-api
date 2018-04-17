# README #

This README would normally document whatever steps are necessary to get your application up and running.

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
npm install --save-dev serverless-wsgi serverless-python-requirements serverless-dynamodb-local
virtualenv venv --python=python3
source venv/bin/activate
pip install flask
pip install boto3
pip freeze > requirements.txt
```
* Test locally:
```
sls wsgi serve
```
* Deploy to AWS:
```
sls deploy
```

### References

* https://serverless.com/blog/flask-python-rest-api-serverless-lambda-dynamodb/