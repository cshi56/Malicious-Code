import yara
from tkinter.filedialog import askopenfilename

def mycallback(data):
    print("Rule: " + str(data['rule']))
    print("Description: " + data['meta']['description'])
    print("Match?: " + str(data['matches']))
    return yara.CALLBACK_CONTINUE

filename = askopenfilename()

rules = yara.compile(filepath='/Users/joecus1/Desktop/Yara-Rules/rules/maldocs/Maldoc_VBA_macro_code.yar')
matches = rules.match(filename,
                      callback=mycallback)
