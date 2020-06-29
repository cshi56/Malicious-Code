
import requests
from tkinter.filedialog import askopenfilename
import time

'''
filename = askopenfilename()

url = 'https://www.virustotal.com/vtapi/v2/file/scan'

params = {'apikey': '52bee9b612bccc94c81f40c73a72b9dc151ce058703cb0125aa6faa2015b4335'}

files = {'file': (filename, open(filename, 'rb'))}

response = requests.post(url, files=files, params=params)

print(response.json())
'''



url = 'https://www.virustotal.com/vtapi/v2/file/report'

params = {'apikey': '52bee9b612bccc94c81f40c73a72b9dc151ce058703cb0125aa6faa2015b4335',
          'resource': 'aabf79901a4aa455373abac04f335be6'}

response = requests.get(url, params=params)

print(response.json())

