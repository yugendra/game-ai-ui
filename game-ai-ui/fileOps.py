import subprocess
import os

def readFile(user):
    lines = ''
    with open(os.getcwd() + '/files/' + user + '.py') as fp:
        for line in fp:
            lines = lines + line
    return lines
    
def writeFile(user, data):
    f = open(os.getcwd() + '/files/' + user + '.py','w')
    f.write(data)
    
def runFile(user):
    result = subprocess.Popen(['python', os.getcwd() + '/files/' + user + '.py'], stdout=subprocess.PIPE)
    stdout = result.communicate()[0]
    return stdout
    
def createUserEnv(user):
    subprocess.Popen(['cp', '-f', os.getcwd() + '/files/code.py', os.getcwd() + '/files/' + user + '.py'], stdout=subprocess.PIPE)