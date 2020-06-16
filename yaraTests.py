import yara

def mycallback(data):
    print(data)
    return yara.CALLBACK_CONTINUE

rules = yara.compile(filepath='/Users/joecus1/Desktop/Yara-Rules/rules/maldocs/Maldoc_VBA_macro_code.yar')
matches = rules.match('/Users/joecus1/Desktop/Malware/rule-06.20.doc',
                      callback=mycallback, which_callbacks=yara.CALLBACK_MATCHES)
