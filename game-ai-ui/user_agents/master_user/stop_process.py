from multiprocessing import Process
from agent import run_agent


if __name__ == '__main__':
    p = Process(target=run_agent, args=(5900, 15900))
    p.daemon = True
    p.start()
    print p.pid
    p.join() # this blocks until the process terminates
    #result = queue.get()
    #print result
