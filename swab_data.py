import requests
import json
import pandas as pd

payload = {
    'grant_type': 'client_credentials',
    'client_id': 'app'
    }

try:
    r = requests.post("http://address/service/get_token",
                      headers={"Content-Type": 'application/x-www-form-urlencoded'},
                      data = payload)

    body = json.loads(r.content)
    token = body["access_token"]
    expiresIn = body["expires_in"]
    print(token)

    url= ""

    r = requests.get(url, headers = {"Authorization":"Bearer " + token}).json()

    df = pd.DataFrame(r)
    df.to_csv('response_python.csv')

except:
    print("Errors")
