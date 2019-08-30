## Local setup

  python3 -m venv env
  source virtual_env/bin/activate
  pip install -r requirements.txt

## Config

  export SF_LOCATIONS_API_KEY="<api_token>"

## Run locally

  serverless invoke local -f films-location --data '{ "queryStringParameters": {"limit":"1"}}'

## Manual Deploy

  sls deploy

## Manual Gateaway Deploy

  aws apigateway create-deployment --rest-api-id agscg4rg20 --stage-name prod