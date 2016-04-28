from flask import Flask, jsonify
from flask import request
import requests
import json
app = Flask(__name__)



subscribers = []
@app.route('/paas/eventSubscriptions', methods=['POST','GET','DELETE'])
def event_subscribe():

    data = json.loads(request.data)
    subscribers.append()
    return "json_data"


@app.route('/paas/callback', methods=['POST','GET'])
def callback():
    data = json.loads(request.data)
    print("eventType: ", data['eventType'], "timestamp: ", data['timestamp'])
    if data['eventType'] == "deployment_info" or data['eventType'] == "deployment_step_success":
        print("deployment_id:", data['plan']['id'])
        app_steps = data["plan"]["steps"]
        for step in app_steps:
            print("step:", step)
        app_actions = data["currentStep"]["actions"]
        for action in app_actions:
            print("action:", action) 

    if data['eventType'] == 'status_update_event':
	print("status",data)
    pri = {
       "group_change_success": "groupId",
        "deployment_info": "currentStep",
        "status_update_event":"appId,taskId,taskStatus",
        "deployment_step_success":"currentStep",
        "deployment_success":"id",
        "api_post_event": "clientIp,uri",
        "app_terminated_event":""
    }

    # keys = pri[data["eventType"]].strip().split(',')
    # for key in keys:
    #     print(data[key])
    # # classifying the events according to the eventType
    # # if "deployment_info" == data['eventType']:
    # #     print(data['currentStep']['steps'])
    #
    return "callback"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=34567, debug=True)
