import json

def handler(event, context):
  response = {
      "hello": "world"
  }

  return json.dumps(response)