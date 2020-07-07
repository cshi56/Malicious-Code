import yara
import os
from tkinter.filedialog import askopenfilename

listMatches = []

def mycallback(data):
    listMatches.append(data['rule'])
    return yara.CALLBACK_CONTINUE


def emptyList():
    for i in range(len(listMatches)):
        listMatches.pop()

def createYaraFiles(directory):
    yaraFiles = [os.path.join(root, name)
                 for root, dirs, files in os.walk(directory)
                 for name in files
                 if name.endswith((".yar"))]
    return yaraFiles

def findMatches(upload, yaraFiles):
    for file in yaraFiles:
        try:
            rule = yara.compile(file)
            matches = rule.match(upload, callback=mycallback, which_callbacks=yara.CALLBACK_MATCHES)
        except:
            pass



def yaraScan():
    emptyList()
    filename = askopenfilename()
    yaraFiles = createYaraFiles('rules')
    findMatches(filename, yaraFiles)
    for match in listMatches:
        print(match)
    return

def maldocsScan(upload):
    emptyList()
    yaraFiles = createYaraFiles('test/analysis/rules/maldocs')
    findMatches(upload, yaraFiles)
    return listMatches