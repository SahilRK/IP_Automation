import requests
import urllib.request
import pandas as pd
import os
import sys
from PIL import Image

#inputDf = pd.read_excel("")

""" curl --location --request POST 'https://api.getharbour.com/v1/onboard/fetchprofileimage' \
--header 'Authorization: Basic cnBhdXNlcjpGRklFREFDRUlFRQ==' \
--header 'Content-Type: application/json' \
--data-raw '["AS675786", "GS10345447"]' """

url = "https://api.getharbour.com/v1/onboard/fetchprofileimage"
method = "POST"
header = {'Authorization' : 'Basic cnBhdXNlcjpGRklFREFDRUlFRQ==', 'Content-Type':'application/json'}
raw_data = '["AS675786", "GS10345447"]'

response = requests.post(url=url, headers=header,data=raw_data)

json_resp = response.json()

print(response.status_code)
print(json_resp["list"])


