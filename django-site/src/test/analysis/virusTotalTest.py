
import requests
from tkinter.filedialog import askopenfilename
import time
import json
import hashlib


def scan(filename):
    url = 'https://www.virustotal.com/vtapi/v2/file/scan'

    params = {'apikey': '52bee9b612bccc94c81f40c73a72b9dc151ce058703cb0125aa6faa2015b4335'}

    files = {'file': (filename, open(filename, 'rb'))}

    response = requests.post(url, files=files, params=params)
    return response.json()

def search(hash):
    url = 'https://www.virustotal.com/vtapi/v2/file/report'

    params = {'apikey': '52bee9b612bccc94c81f40c73a72b9dc151ce058703cb0125aa6faa2015b4335',
              'resource': hash}

    response = requests.get(url, params=params)
    return response.json()

def VTScan(filename, hash):
    print("First search")
    response = search(hash)
    if response['response_code'] is not 1:
        print("Scanning file")
        print(scan(filename))
        i = 0
        while i < 12:
            i += 1
            time.sleep(20)
            response = search(hash)
            if response['response_code'] is 1:
                break;
    detections = 0
    if response['response_code'] is 1:
        for key in response['scans']:
            if response['scans'][key]['detected'] is True:
                detections += 1
    else:
        detections = -1
    return [detections, response['permalink']]

'''
#get file
filename = askopenfilename()

#get hash
sha256_hash = hashlib.sha256()
a_file = open(filename, "rb")
content = a_file.read()
sha256_hash.update(content)

#search and scan
print("First search")
response = search(sha256_hash.hexdigest())
if response['response_code'] is not 1:
    print("Scanning file")
    print(scan(filename))
    print(sha256_hash.hexdigest())
    i = 0
    while i < 12:
        i += 1
        time.sleep(20)
        response = search(sha256_hash.hexdigest())
        print(response)
        if response['response_code'] is 1:
            break;
print(response)
detections = 0
for key in response['scans']:
    if response['scans'][key]['detected'] is True:
        detections += 1
print(detections)
print(response['permalink'])
'''