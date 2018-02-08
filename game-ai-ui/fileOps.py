import subprocess
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

def readFile(user):
    lines = ''
    with open(script_dir + '/files/' + user + '.py') as fp:
        for line in fp:
            lines = lines + line
    return lines
    
def writeFile(user, data):
    f = open(script_dir + '/files/' + user + '.py','w')
    f.write(data)
    
def runFile(user):
    result = subprocess.Popen(['python', script_dir + '/files/' + user + '.py'], stdout=subprocess.PIPE)
    stdout = result.communicate()[0]
    return stdout
    
def createUserEnv(user):
    subprocess.Popen(['cp', '-n', script_dir + '/files/code.py', script_dir + '/files/' + user + '.py'], stdout=subprocess.PIPE)