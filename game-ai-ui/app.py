import MySQLdb
import MySQLdb.cursors
from flask import Flask, render_template, request, make_response, jsonify, Response
from flask_socketio import SocketIO
from fileOps import readFile, writeFile, runFile, createUserEnv
from env_ops import create_env, remove_env, is_env_running, get_env_list, remove_env_in_bulk, get_vnc_port, get_host_ssh_port, execute_code
from subprocess import Popen
from agent_ops import is_agent_running, start_agent, stop_agent
from time import sleep
from log_reader import LogReader
from threading import Thread
from get_last_log import get_last_log

from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from instagram import getfollowedby, getname

app = Flask(__name__)

socketio = SocketIO(app)
#log_thread = Thread()

database = MySQLdb.connect(host = "localhost", 
	user = "root",
	passwd = "devops123", 
	db = "user_creds", 
	cursorclass = MySQLdb.cursors.DictCursor)
cursor = database.cursor()



@app.route('/', methods=['GET', 'POST'])
def home():
        """ Session control"""
        if not session.get('logged_in'):
                print("=====================section 1 ========================")
                return render_template('index.html')
        else:
                if request.method == 'POST':
                        print("=====================section 2 ========================")
                        username = getname(request.form['username'])
                        return render_template('index.html', data=getfollowedby(username))
                print("=====================section 3 ========================")
                return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
        """Login Form"""
        if request.method == 'GET':
                return render_template('login.html')
        else:
                name = request.form['username']
                passw = request.form['password']
                try:
                        cursor.execute("SELECT password FROM user_table WHERE username = '"+name+"';")
                        data = cursor.fetchall()
                        print(data[0]['password'])
                        
                        if data is not None and data[0]['password'] == passw:
                                session['logged_in'] = True
                                user = request.form['username']
                                vnc_port = get_vnc_port(user)
                                ssh_port = get_host_ssh_port(user)
                                createUserEnv(user)
                                resp = make_response(render_template('playArea.html'))
                                resp.set_cookie('userID', user)
                                resp.set_cookie('vnc_port', vnc_port)
                                resp.set_cookie('ssh_port', ssh_port)
                                print(resp)
                                return resp

                                #return redirect(url_for('home'))
                        else:
                                return 'Dont Login'
                except:
                        return "Dont Login"

@app.route('/register/', methods=['GET', 'POST'])
def register():
        """Register Form"""
        if request.method == 'POST':
                user=request.form['username']
                passwd=request.form['password']
                
                cursor.execute("INSERT INTO user_table (username, password, container_id, vnc_port, ssh_port, is_container_running) VALUES ('"+user+"', '"+passwd+"','null',0,0,'0');")
                return render_template('login.html')
        return render_template('register.html')

@app.route("/logout")
def logout():
        """Logout Form"""
        session['logged_in'] = False
        return redirect(url_for('home'))


@app.route('/nocontainer')
def nocontainer():
    return render_template('nocontainer.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/get_env_list', methods=['POST'])
def env_list():
    env_list = get_env_list()
    return jsonify(env_list)

@app.route('/remove_envs', methods=['POST'])
def remove_envs():
    envs = request.json['data']
    remove_env_in_bulk(envs)
    return render_template('admin.html')

@app.route('/playArea', methods=["POST"])
def playArea():
    user = request.form['username']
    vnc_port = get_vnc_port(user)
    ssh_port = get_host_ssh_port(user)
    createUserEnv(user)
    resp = make_response(render_template('playArea.html'))
    resp.set_cookie('userID', user)
    resp.set_cookie('vnc_port', vnc_port)
    resp.set_cookie('ssh_port', ssh_port)
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


@app.route('/delete', methods = ["POST"])
def delete():
    projectname=request.form['projectname']
    print(projectname)
    try:
        user = request.cookies['userID']
        print(user)
    except:
        return False

    if is_env_running(user):
        print("env already running!")
        remove_env(user)
        sleep(2)

    print("sending delete resp back")
    resp = make_response(render_template('playArea.html'))
    resp.set_cookie('nocontainer', str("No container running now."))
    ## Update user info
    query = "update  user_creds.user_table SET container_id = '' , vnc_port = '' , ssh_port = '' , is_container_running = 0 where username = '"+user+"';"
    print(query)
    cursor.execute(query)

    return resp


    

@app.route('/run', methods=["POST"])
def run():
    projectname=request.form['projectname']
    print(projectname)
    print("reading cookies...."+str(request.cookies['userID']))
    try:
        user = request.cookies['userID']
        #writeFile(user, request.form['data'])
        print("file updated")
        print(user)
    except:
        return False

    try:
        pid = request.cookies['PID']
        print(pid)
    except:
        pid = None

    #if is_agent_running(pid): stop_agent(pid)
    
    if is_env_running(user):
        print("env already running!")
        #remove_env(user)
        writeFile(user, request.form['data'])
        execute_code(user,projectname)
        resp = make_response(render_template('playArea.html'))
        return resp
    else:
        vnc_port, info_channel ,ssh_port, container_id= create_env(user, projectname=projectname)
        print("env created.")
        sleep(2)
        print("sending resp back")
        resp = make_response(render_template('playArea.html'))
        resp.set_cookie('vnc_port', str(vnc_port))
        resp.set_cookie('ssh_port', str(ssh_port))
        resp.set_cookie('info_channel', str(info_channel))
        resp.set_cookie('PID', str(pid))

        query = "update  user_creds.user_table SET container_id = '"+str(container_id)+"' , vnc_port = '"+str(vnc_port)+"' , ssh_port = '"+str(ssh_port)+"' , is_container_running = 1 where username = '"+user+"';"
        print(query)
        cursor.execute(query)
        print(request.form['data'])
        writeFile(user, request.form['data'])
        execute_code(user,projectname)
        return resp

@app.route('/getLog', methods=["POST"])
def getLog():
    user = request.cookies['userID']
    loglines = get_last_log(user)
    return loglines

@app.route('/getcontainerLog', methods=["POST"])
def getLog():
    user = request.cookies['userID']
    loglines = get_last_log(user)
    return loglines


@socketio.on('connect', namespace='/getlogs')
def connect():
    #global log_thread
    log_thread = Thread()
    user = request.cookies['userID']
    print "Client connected"
    if not log_thread.isAlive():
        log_thread = LogReader(socketio, user)
        log_thread.start()

@socketio.on('disconnect', namespace='/getlogs')
def disconnect():
    """
        Operations after client disconnect.
    """
    #TODO: detect if client is closed
    print('Client disconnected')

if __name__ == '__main__':
    app.debug = True
    app.secret_key = "123"
    socketio.run(app, host='0.0.0.0',debug=True)

