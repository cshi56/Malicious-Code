import yara
from tkinter.filedialog import askopenfilename
import os

def mycallback(data):
    print(data)
    return yara.CALLBACK_CONTINUE

'''
directory = '/Users/joecus1/Desktop/Yara-Rules/rules/maldocs/'
filelist = os.listdir(directory)
dict = {}

for i in range(len(filelist)):
    dict["file" + str(i)] = \
        '/Users/joecus1/Desktop/Yara-Rules/rules/maldocs/' + filelist[i]
'''

filename = askopenfilename()

rules = yara.compile(filepath='/Users/joecus1/Desktop/Yara-Rules/rules/maldocs/Maldoc_VBA_macro_code.yar')

# rules = yara.compile(filepaths=dict)

matches = rules.match(filename,
                      callback=mycallback, which_callbacks=yara.CALLBACK_MATCHES)
