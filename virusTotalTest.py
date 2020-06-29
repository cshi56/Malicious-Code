import requests

url = 'https://www.virustotal.com/vtapi/v2/file/report'

params = {'apikey': '52bee9b612bccc94c81f40c73a72b9dc151ce058703cb0125aa6faa2015b4335', 'resource': '99017f6eebbac24f351415dd410d522d'}

response = requests.get(url, params=params)

print(response.json())
