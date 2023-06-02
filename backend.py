from flask import Flask
from flask import request
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app, supports_credentials=True)
global data
data = []

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/get", methods=['POST'])
def get():
    global data
    # print(request.json)
    data = modbus.get_data()
    if data == None or len(data) < LEN :
        return [0]*LEN
    data = [i for i in data]
    return data

@app.route("/set", methods=['POST'])
def set():
    req = request.json
    if req: 
        value = [int(req["start"]), int(req["motor"]), int(req["heat"]), int(req["relay1"]), int(req["relay2"])]
        modbus.writeMultiple(19, len(value), value) # %MQW19-23
        return "ok"
    else:
        return "bad request"

if __name__ == "__main__":
    LEN = 13
    from communicator import ModbusModule
    modbus = ModbusModule("192.168.1.1", 502)
    modbus.start(0, LEN)
    app.run(host='0.0.0.0', port=5000, debug=True)