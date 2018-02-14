from subprocess import Popen
from agent import run_agent


#def start_proc():
if __name__ == '__main__':
    p = Popen(['python', '/root/game-ai/game-ai-ui/game-ai-ui/user_agents/master_user/agent.py', '5900', '15900'])
    print p.pid
    
