from flask import Flask, render_template, request, make_response, jsonify
from flask_socketio import SocketIO
from fileOps import readFile, writeFile, runFile, createUserEnv
from env_ops import create_env, remove_env, is_env_running, get_env_list, remove_env_in_bulk, get_vnc_port
from subprocess import Popen
from agent_ops import is_agent_running, start_agent, stop_agent
from time import sleep

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'yugendra'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/get_env_list', methods=['POST'])
def env_list():
    env_list = get_env_list()
    print env_list
    return jsonify(env_list)

@app.route('/remove_envs', methods=['POST'])
def remove_envs():
    envs = request.json['data']
    remove_env_in_bulk(envs)
    return render_template('admin.html')

@app.route('/playArea', methods=["POST"])
def login():
    print request.form
    user = request.form['user']
    vnc_port = get_vnc_port(user)
    createUserEnv(user)
    resp = make_response(render_template('playArea.html'))
    resp.set_cookie('userID', user)
    resp.set_cookie('vnc_port', vnc_port)
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
    try:
        user = request.cookies['userID']
    except:
        return False

    try:
        pid = request.cookies['PID']
    except:
        pid = None
    
    #if is_agent_running(pid): stop_agent(pid)
    if is_env_running(user):
        remove_env(user)
        sleep(2)
    
    vnc_port, info_channel = create_env(user)
    sleep(2)
    #pid = start_agent(user, vnc_port, info_channel)
    
    resp = make_response(render_template('playArea.html'))
    resp.set_cookie('vnc_port', str(vnc_port))
    resp.set_cookie('info_channel', str(info_channel))
    resp.set_cookie('PID', str(pid))
    
    return resp


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
