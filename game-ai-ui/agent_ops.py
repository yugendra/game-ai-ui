from psutil import Process, pid_exists
from subprocess import Popen

def is_agent_running(pid):
    return pid_exists(pid)

def start_agent(user, vnc_port, info_channel):
    agent = '/root/game-ai/game-ai-ui/game-ai-ui/user_agents/' + user + '/agent.py'
    p = Popen(['python', agent, str(vnc_port), str(info_channel)])
    return str(p.pid)

def stop_agent(pid):
    p = Process(pid)
    p.kill()
    return True
