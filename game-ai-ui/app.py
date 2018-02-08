from flask import Flask, render_template, request, make_response
from flask_socketio import SocketIO
from fileOps import readFile, writeFile, runFile, createUserEnv

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
    user = request.cookies['userID']
    result = runFile(user)
    return result


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')