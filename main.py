from flask import Flask, jsonify, request
from time import sleep
import erv
from concurrent.futures import ThreadPoolExecutor

# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
executor = ThreadPoolExecutor(1)

app = Flask(__name__)


@app.route('/state')
def check_state():
    state = erv.checkpinstatus()
    return jsonify({'pin state': state})


@app.route('/fan/start')
def fan():
    req_data = request.get_json()
    timer = req_data['time']
    executor.submit(start_fan, timer)
    return jsonify({'state': 'fan started'})


# submitting data not query string
@app.route('/form', methods=['POST', 'GET'])
def form():
    req_data = request.get_json()
    timer = req_data['time']
    executor.submit(custom_task, timer)
    return jsonify({'duration': timer})


@app.route('/jobs')
def run_jobs():
    return jsonify({'key': 'value'})


@app.route('/custom/<int:duration>')
def run_custom(duration):
    executor.submit(custom_task, duration)
    return jsonify({'duration': duration})


def start_fan(timer):
    if not erv.checkpinstatus():
        erv.relay(timer)
    else:
        return jsonify({
            'state': 'already running'
        })


def custom_task(timer):
    print('sleeping for {} seconds'.format(timer))
    sleep(int(timer))
    print('done!')


if __name__ == '__main__':
    # cleanup pins
    erv.pincleanup()
    app.run(debug=True, host='0.0.0.0')
