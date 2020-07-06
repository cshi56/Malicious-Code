import yara
import os
from tkinter.filedialog import askopenfilename

def mycallback(data):
    print(data)
    listMatches.append(data)
    return yara.CALLBACK_CONTINUE


listMatches = []

def yaraScan(upload, debug=False):
    if(debug):
        filename = askopenfilename()
        yarafiles = [os.path.join(root, name)
                     for root, dirs, files in os.walk('rules')
                     for name in files
                     if name.endswith((".yar"))]
        for file in yarafiles:
            try:
                rule = yara.compile(file)
                matches = rule.match(filename, callback=mycallback, which_callbacks=yara.CALLBACK_MATCHES)
            except:
                pass
        for match in listMatches:
            print(match)
        return


    print("Running Yara tests")
    yarafiles = [os.path.join(root, name)
             for root, dirs, files in os.walk('test/analysis/rules/maldocs')
             for name in files
             if name.endswith((".yar"))]
    for file in yarafiles:
        try:
            rule = yara.compile(file)
            matches = rule.match(upload, callback=mycallback, which_callbacks=yara.CALLBACK_MATCHES)
        except:
            pass
    return listMatches
