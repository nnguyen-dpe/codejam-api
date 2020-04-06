#!/bin/bash
cd codejam-api
pwd
source venv/bin/activate
sls wsgi serve --host=0.0.0.0