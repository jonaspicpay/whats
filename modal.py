
import json
import requests

response = requests.get("http://vps4782.publiccloud.com.br/send/")
json_data = json.loads(response.text)
for user in json_data:
    print user['mensagem']
