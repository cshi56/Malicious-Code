import yara
import os
from tkinter.filedialog import askopenfilename

def mycallback(data):
    print(data)
    return yara.CALLBACK_CONTINUE



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
        return



    print("Running Yara tests")
    print(upload)
    yarafiles = [os.path.join(root, name)
             for root, dirs, files in os.walk('test/analysis/rules')
             for name in files
             if name.endswith((".yar"))]
    for file in yarafiles:
        try:
            rule = yara.compile(file)
            matches = rule.match('uploads/' + upload, callback=mycallback, which_callbacks=yara.CALLBACK_MATCHES)
        except:
            pass