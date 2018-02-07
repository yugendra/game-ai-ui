from flask import Flask, render_template, request
from flask_socketio import SocketIO
from fileOps import readFile, writeFile, runFile

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'yugendra'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/getFile')
def getFile():
    return readFile()
    
@app.route('/saveFile', methods=["POST"])
def saveFile():
    writeFile(request.form['data'])
    return 'True'
    
@app.route('/run', methods=["POST"])
def run():
    result = runFile()
    return result


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')