```
import requests

headers = {'Content-Type': 'application/json'}

data = {"name": "Item 1", "description": "This is a test item."}

response = requests.post("https://example.com/api/items", headers=headers, json=data)
print(response.text)
```