from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='', static_url_path='')
CORS(app)

@app.route('/')
def main():
    return app.send_static_file('index.html')

@app.route('/create', methods=["POST"])
def createVM():
    vm = request.get_json()
    return_code = os.system("onevm create --name " + str(vm['name']) + " --cpu " + str(vm['cpu'])
                             + " --memory " + str(vm['memory']) +  " --user " + str(vm['username']) + " --password " + str(vm['password']) + " --disk oneadmin[alpinelinux]")
    if return_code == 0:
        return jsonify(), 200
    
    return jsonify(), 400

@app.route('/register', methods=["POST"])
def registerUser():
    user = request.get_json()
    return_code = os.system("oneuser create " + str(user['username']) + " " + str(user['password']))
    if return_code == 0:
        return jsonify(), 200
    
    return jsonify(), 400

@app.route('/login', methods=["POST"])
def loginUser():
    user = request.get_json()
    command = "onevm list --user " + user['username'] + " --password " + user['password']
    return_code = os.system(command)
    if return_code == 0:
        result = os.popen(command).read()
        return jsonify(result), 200
    
    return jsonify(), 400

@app.route('/vms', methods=["POST"])
def getVms():
    user = request.get_json()
    command = "onevm list --user " + user['username'] + " --password " + user['password']
    os.system(command)
    result = os.popen(command).read()
    return jsonify(result), 200

@app.route('/poweron', methods=["POST"])
def poweron():
    vm = request.get_json()
    return_code = os.system("onevm resume " + str(vm["id"]))
    if return_code == 0:
        return jsonify(), 200
    
    return jsonify, 400

@app.route('/poweroff', methods=["POST"])
def poweroff():
    vm = request.get_json()
    return_code = os.system("onevm poweroff " + str(vm["id"]))
    if return_code == 0:
        return jsonify(), 200
    
    return jsonify, 400

@app.route('/delete', methods=["POST"])
def deleteVM():
    vm = request.get_json()
    return_code = os.system("onevm terminate " + str(vm["id"]) + " --hard")
    if return_code == 0:
        return jsonify(), 200
    
    return jsonify(), 400


@app.route('/hosts', methods=["POST"])
def getHosts():
    user = request.get_json()
    command = "onehost list --user " + user['username'] + " --password " + user['password']
    return_code = os.system(command)
    if return_code == 0:
        result = os.popen(command).read()
        line_count = 0
        for i in range(len(result)):
            if result[i] == '\n':
                line_count += 1
        if line_count < 2:
            return jsonify(), 400
        
        return jsonify(result), 200
    
    return jsonify(), 400


@app.route('/users', methods=["POST"])
def getUsers():
    user = request.get_json()
    command = "oneuser list --user " + user['username'] + " --password " + user['password']
    return_code = os.system(command)
    if return_code == 0:
        result = os.popen(command).read()
        line_count = 0
        for i in range(len(result)):
            if result[i] == '\n':
                line_count += 1
        if line_count < 3:
            return jsonify(), 400
        
        return jsonify(result), 200
    
    return jsonify(), 400

@app.route('/deleteuser', methods=["POST"])
def deleteUser():
    id = request.get_json()
    return_code = os.system("oneuser delete " + str(id["id"]))
    if return_code == 0:
        return jsonify(), 200
    
    return jsonify(), 400


if __name__ == '__main__':
    app.run(threaded=True, port=5000, host="0.0.0.0")
