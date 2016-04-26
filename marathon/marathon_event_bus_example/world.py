from flask import Flask, jsonify
from flask import request
import requests
import json
app = Flask(__name__)


headers = {'content-type' : 'application/json'}
subscribers = []

@app.route('/paas/eventSubscriptions', methods=['POST','GET','DELETE'])
def event_subscribe():
    if request.method == 'POST':
        print(request.data)
        data = json.loads(request.data)
        print(data)
        subscribers.append(data['url'])
    if request.method == 'GET':
        pass
    if request.method == 'DELETE':
        data = json.loads(request.data)
        print(data)
        subscribers.append()
    for i in subscribers:
        print(i)
    return "json_data"


@app.route('/paas/callback', methods=['POST','GET'])
def callback():
    data = json.loads(request.data)
    if data['eventType'] == 'status_update_event':
        print(data)
        for url in subscribers:
            print(url)
            try:
                r = requests.post(url, data=json.dumps(data), headers=headers)
            except Exception as e:
                print(e)
    return "hello world!"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=34567, debug=True)
