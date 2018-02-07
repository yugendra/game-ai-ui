import subprocess

def readFile():
    lines = ''
    with open('files/code.py') as fp:
        for line in fp:
            lines = lines + line
    print lines
    return lines
    
def writeFile(data):
    f = open('files/code.py','w')
    f.write(data)
    
def runFile():
    result = subprocess.Popen(['python', 'files/code.py'], stdout=subprocess.PIPE)
    stdout = result.communicate()[0]
    return stdout
    