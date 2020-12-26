from flask import Flask, request, make_response, jsonify
from browser import firefoxdriver

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
f = firefoxdriver()


@app.route('/judge_doc', methods=['GET'])
def judge_doc():
    key_word = request.args["query"]
    data = f.get_data(key_word)
    header = {
        "Content-Type": "application/json;charset=utf-8"
    }
    return jsonify({"result": data}), 200, header


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
