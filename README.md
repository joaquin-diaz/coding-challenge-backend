## Local setup
First create a new python virtual environment then install the requirements. 

> python3 -m venv env
> source virtual_env/bin/activate
> pip install -r requirements.txt
   
## Run locally
Runs a local server simulating an AWS Gateway API. The server is exposed at: http://localhost:3000
`serverless offline`

## Run tests
`python -m unittest`

## Manual Deploy
To run the manual deploy
`sls deploy`

## Config
 - `export SF_LOCATIONS_API_KEY="<api_token>" `
 - `export GOOGLE_API_KEY="<api_key>"`

If you want to deploy manually:

 - `export AWS_SECRET_KEY_ID="<key_id>"`
 - `export AWS_SECRET_ACCESS_KEY="secret_key"`
 - `export AWS_DEFAULT_REGION="sa-east-1"`

## Circle CI Integration
master@CirleCI [![CircleCI](https://circleci.com/gh/joaquin-diaz/coding-challenge-backend/tree/master.svg?style=svg)](https://circleci.com/gh/joaquin-diaz/coding-challenge-backend/tree/master)
Just to simplify the workflow, the API is deployed on every merge to master