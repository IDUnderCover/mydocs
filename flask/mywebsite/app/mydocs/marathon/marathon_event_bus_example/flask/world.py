import json

import requests
from flask import Flask
from flask import request

import config

app = Flask(__name__)
headers = {'content-type' : 'application/json'}
subscribers = config.subscribers

def success(info):
    return json.dumps({"status":"success","info":info})

def failed(info):
    return json.dumps({"status":"failed","info":info})

@app.route('/paas/eventSubscriptions', methods=['POST','GET','DELETE'])
def event_subscribe():
    try:
        if request.method == 'POST':
            data = json.loads(request.data)
            subscribers.append(data['url'])
            return success("subscribe successfully"), 200 
        if request.method == 'GET':
            return success(subscribers), 200
        if request.method == 'DELETE':
            data = json.loads(request.data)
            subscribers.remove(data['url'])
            return success("delete the url ", + data['url'], + " successfully"), 200
    except Exception as  e:
        return failed(e.__str__()), 500


@app.route('/paas/callback', methods=['POST','GET'])
def callback():
    data = json.loads(request.data)
   # print(data)
    if data['eventType'] == 'status_update_event':
        result = {"containerid":data['appId'],
                  "acttype":data["taskStatus"]}
        for url in subscribers:
            try:
                for i in range(3):
                    r = requests.post(url, data=result,timeout=1)
                    if r.ok:
                        print("response from " + url + "with content: " + r.content)
                        break
                    print("request url " + url + " failed  at " + str(i+1) + " time")
                    #time.sleep(2000)
            except Exception as e:
                print(e)
    return "success", 200

@app.route('/healthy', methods=['GET'])
def healthy():
    return "healthy",200

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=34567 )
