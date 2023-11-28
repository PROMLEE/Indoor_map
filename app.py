from flask import Flask, request, jsonify
# way.py에서 process_data 함수를 임포트합니다.
from way import process_data

app = Flask(__name__)

@app.route('/run-way', methods=['POST'])
def run_way():
    data = request.json
    result = process_data(data['value1'], data['value2'], data['value3'], data['value4'])
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
