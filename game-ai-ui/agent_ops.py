from psutil import Process, pid_exists
from subprocess import Popen
import os

script_dir = os.path.dirname(os.path.realpath(__file__))

def is_agent_running(pid):
    if not pid:
        return False
    return pid_exists(int(pid))

def start_agent(user, vnc_port, info_channel):
    agent = script_dir + '/user_agents/' + user + '/agent.py'
    p = Popen(['python', agent, str(vnc_port), str(info_channel)])
    return p.pid

def stop_agent(pid):
    p = Process(int(pid))
    p.kill()
    return True
