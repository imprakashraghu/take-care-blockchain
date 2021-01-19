from flask import Flask
from flask import request
from flask import make_response, jsonify
from datetime import date
import json
import requests
from web3 import Web3
from datetime import date
from flask_cors import CORS, cross_origin

# Blockchain connction
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))
address='0xA9AF4C327c71f3EB3216ad87319fC83CB2CDeE54'
abi=json.loads('[{"constant":true,"inputs":[{"name":"emp_id","type":"string"}],"name":"readGeneralRecord","outputs":[{"name":"","type":"string[]"},{"name":"","type":"string[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"emp_id","type":"string"}],"name":"readRecord","outputs":[{"name":"","type":"string[]"},{"name":"","type":"string[]"},{"name":"","type":"string[]"},{"name":"","type":"string[]"},{"name":"","type":"string[]"},{"name":"","type":"string[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"hr_value","type":"string"},{"name":"bp_value","type":"string"},{"name":"temp_value","type":"string"},{"name":"gl_value","type":"string"},{"name":"ox_value","type":"string"},{"name":"res_value","type":"string"},{"name":"steps_value","type":"string"},{"name":"create_value","type":"string"},{"name":"emp_id","type":"string"}],"name":"addRecord","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"}]')
privatekey='c1ed552d5497d77c288c5a2a0a745cf1247cf016ce2fc36cb9eedf19c0082179'
# contract connection eshtablishment
contract=web3.eth.contract(address=address,abi=abi)
web3.eth.defaultAccount=web3.eth.accounts[0]

app = Flask("db")
CORS(app, support_credentials=True)

@app.route("/add", methods=["POST"])
def addRecord():
    try:
        req = request.json
        emp_id = req['emp_id']
        hr = req['hr']
        bp = req['bp']
        temp = req['temp']
        gl = req['gl']        
        ox = req['ox']
        res = req['res']
        steps = req['steps']        
        create = req['create']        
        records = contract.functions.addRecord(hr, bp, temp, gl, ox, res, steps, create, emp_id).transact()
        return "record added successfully"
    except:        
        return "something went wrong"

@app.route("/view", methods=["GET"])
@cross_origin(supports_credentials=True)
def getRecords():        
    empId = request.args.get('emp_id')
    records = []    
    generalRecords = []
    try:
        records = contract.functions.readRecord(empId).call()                    
        generalRecords = contract.functions.readGeneralRecord(empId).call() 
        result = []
        for i in range(0, len(records[0])):
            stat = {}
            stat['heartRate'] = records[0][i]
            stat['bloodPressure'] = records[1][i]
            stat['bodyTemperature'] = records[2][i]
            stat['gulcose'] = records[3][i]
            stat['oxygen'] = records[4][i]
            stat['respiration'] = records[5][i]                
            stat['steps'] = generalRecords[0][i]
            stat['created'] = generalRecords[1][i]                                                                                                        
            result.append(stat)                 
        pData = requests.get('https://api.npoint.io/c2964d73bfb19f317f87/')               
        return jsonify({ "data": result, "p_data": pData.json() })
    except:
        return "something went wrong"

app.run(host='0.0.0.0', port=5050)