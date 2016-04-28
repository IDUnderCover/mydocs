from flask import Flask,request
import json

app = Flask(__name__)


@app.route('/mycallback',methods=['POST'])
def callback():
    data = json.loads(request.data)
    print(data)
    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=34568, debug=True)
