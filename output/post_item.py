def post_item(url, data):
  import json
  import requests
  payload = json.dumps(data)
  response = requests.post(url, headers={'Content-Type': 'application/json'}, data=payload)
  return response.json()