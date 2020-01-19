from flask import Flask, jsonify, request
from time import sleep
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


@app.route('/state')
def check_state():
    state = erv.checkpinstatus()
    return jsonify({'pin state': state})


@app.route('/fan/start')
def fan():
    req_data = request.get_json()
    timer = req_data['time']

    if erv.checkpinstatus() == 0:
        executor.submit(start_fan, timer)
        return jsonify({'state': 'fan started', 'time': timer})
    else:
        return jsonify({'state': 'already running'})


@app.route('/fan/add')
def fan_add():
    req_data = request.get_json()
    timer = req_data['time']

    #check state, won't add time if its not running
    if erv.checkpinstatus() == 0:
        return jsonify({'state': 'not started'})
    else:
        executor.submit(add_time_to_fan, timer)
        return jsonify({'state': 'time added', 'time': timer})


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


def add_time_to_fan(timer):
    print('adding time')
    erv.add_time(timer)


def start_fan(timer):
    print('starting fan function')
    # erv.relay(timer)
    # if its running already don't let it run again
    # if you want it to queue up additional, change executor to 1
    erv.relay(timer)
    print('stopping fan function')


def custom_task(timer):
    print('sleeping for {} seconds'.format(timer))
    sleep(int(timer))
    print('done!')


if __name__ == '__main__':
    # cleanup pins
    erv.pincleanup()
    app.run(debug=True, host='0.0.0.0')
