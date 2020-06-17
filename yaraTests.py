import yara
from tkinter.filedialog import askopenfilename
import os

def mycallback(data):
    print(data)
    return yara.CALLBACK_CONTINUE


directory = '/Users/joecus1/Desktop/Yara-Rules/rules/maldocs/'
files = os.listdir(directory)

filename = askopenfilename()

# rules = yara.compile(filepath='/Users/joecus1/Desktop/Yara-Rules/rules/maldocs/Maldoc_VBA_macro_code.yar')

# rules = yara.compile(filepaths=dict)

for file in files:
    try:
        rule = yara.compile(filepath=directory + file)
        matches = rule.match(filename,callback=mycallback, which_callbacks=yara.CALLBACK_MATCHES)
    except:
        print(file + " not working")
