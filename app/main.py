from flask import Flask, jsonify, request
from time import sleep
from log import configure_logging
import erv
from concurrent.futures import ThreadPoolExecutor

'''
so with more than one thread it will run the "start" multiple times, but
if there is only one it will queue up behind the first so if you ask for 10
minutes twice it will go for 20, no matter when you ask for the second 20
'''

# DOCS https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor
executor = ThreadPoolExecutor(1)

app = Flask(__name__)
configure_logging(app)

@app.route('/state', methods=['GET'])
def check_state():
    state = erv.checkpinstatus()
    return jsonify({'pin state': state})


@app.route('/fan/start', methods=['POST'])
def fan():
    req_data = request.get_json()
    timer = req_data['time']
    timer = int(timer)

    if erv.checkpinstatus() == 0:
        executor.submit(start_fan, timer)
        return jsonify({'state': 'fan started', 'time': timer})
    else:
        return jsonify({'state': 'already running'})


@app.route('/fan/add', methods=['POST'])
def fan_add():
    req_data = request.get_json()
    timer = req_data['time']
    timer = int(timer)

    #check state, start with that time
    if erv.checkpinstatus() == 0:
        executor.submit(start_fan, timer)
        return jsonify({'state': 'time added', 'time': timer})

    else:
        executor.submit(add_time_to_fan, timer)
        return jsonify({'state': 'time added', 'time': timer})


@app.route('/fan/stop', methods=['POST'])
def fan_stop():
    executor.submit(stop_fan)
    state = erv.checkpinstatus()
    return jsonify({'state': state})


@app.route('/status', methods=['GET'])
def health_state():
    return jsonify({'health': 'up'})

def add_time_to_fan(timer):
    timer *= 60
    erv.add_time(timer)


def start_fan(timer):
    print('starting fan function')
    timer *= 60
    erv.relay(timer)

def stop_fan():
    erv.stop_fan()


if __name__ == '__main__':
    erv.pincleanup()
    app.run(debug=True, host='0.0.0.0')
