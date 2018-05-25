import subprocess
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

def readFile(user):
    lines = ''
    with open(script_dir + '/user_agents/' + user + '/rdata/script.R') as fp:
        for line in fp:
            lines = lines + line
    return lines
    
def writeFile(user, data):
    f = open(script_dir + '/user_agents/' + user + '/rdata/script.R','w')
    f.write(data)
    
def runFile(user):
    result = subprocess.Popen(['python', script_dir + '/user_agents/' + user + '/agent.py'], stdout=subprocess.PIPE)
    stdout = result.communicate()[0]
    return stdout
    
def createUserEnv(user):
    subprocess.Popen(['cp', '-rn', script_dir + '/user_agents/master_user', script_dir + '/user_agents/' + user ], stdout=subprocess.PIPE)
