from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO
from fileOps import readFile, writeFile, runFile, createUserEnv
from env_ops import create_env, remove_env, is_env_running
from subprocess import Popen
from agent_ops import is_agent_running, start_agent, stop_agent
from time import sleep

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'yugendra'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/playArea', methods=["POST"])
def login():
    print request.form
    user = request.form['user']
    createUserEnv(user)
    resp = make_response(render_template('playArea.html'))
    resp.set_cookie('userID', user)
    return resp

@app.route('/getFile', methods=["POST"])
def getFile():
    user = request.cookies['userID']
    return readFile(user)
    
@app.route('/saveFile', methods=["POST"])
def saveFile():
    user = request.cookies['userID']
    writeFile(user, request.form['data'])
    return 'True'
    
@app.route('/run', methods=["POST"])
def run():
    if request.cookies['userID']:
        user = request.cookies['userID']
    else:
        return "500: Internal Server Error."

    if request.cookies['PID']: pid = request.cookies['PID']
    
    if is_agent_running(int(pid)): stop_agent(int(pid))
    if is_env_running(user):
        remove_env(user)
        sleep(2)
    
    vnc_port, info_channel = create_env(user)
    sleep(2)
    pid = start_agent(user, vnc_port, info_channel)
    
    resp = make_response(render_template('playArea.html'))
    resp.set_cookie('vnc_port', str(vnc_port))
    resp.set_cookie('info_channel', str(info_channel))
    resp.set_cookie('PID', str(pid))
    
    return resp


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
