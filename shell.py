# This is the basic shell for MxSL
from source import main

while True:
    text = input('mxsl > ')
    if text.strip() == '': continue
    result, error = main.run('<stdin>', text)

    if error:
        print(error.as_string())
    elif result:
        if len(result.elements) == 1:
            print(result.elements[0])
        else:
            print(result)
