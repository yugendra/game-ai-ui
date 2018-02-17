from psutil import Process, pid_exists
from subprocess import Popen

def is_agent_running(pid):
    if not pid:
        return False
    return pid_exists(int(pid))

def start_agent(user, vnc_port, info_channel):
    agent = '/root/game-ai/game-ai-ui/game-ai-ui/user_agents/' + user + '/agent.py'
    p = Popen(['python', agent, str(vnc_port), str(info_channel)])
    return p.pid

def stop_agent(pid):
    p = Process(int(pid))
    p.kill()
    return True
