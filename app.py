from flask import Flask, render_template, request, jsonify, Response
from threading import Timer
from queue import Queue
from adafruit_servokit import ServoKit

import os

app = Flask(__name__)

kit = ServoKit(channels=16)
is_driving = False
msg_queue = Queue()

resting_throttle = [0.07, 0.07]

@app.route("/")
def main():
   templateData = {}
   return render_template('main.html', **templateData)

@app.route("/actions/shutdown", methods=["POST"])
def action_shutdown():
    os.system("sudo shutdown -h now")

@app.route("/actions/upgrade", methods=["POST"])
def action_upgrade():
    os.system("git pull")
    exit()

@app.route("/actions/drive", methods=["POST"])
def action_drive():
    is_driving = True
    kit.continuous_servo[0].throttle = 0.2
    kit.continuous_servo[1].throttle = -0.2
    kit.servo[15].angle = 0
    msg_queue.put("driving")
    drive_timer = Timer(2, drive_timeout)
    drive_timer.start()

    return jsonify([])

@app.route("/actions/left", methods=["POST"])
def action_left():
    is_driving = True
    kit.continuous_servo[0].throttle = 0
    kit.continuous_servo[1].throttle = -0.5
    kit.servo[15].angle = 0
    msg_queue.put("left")
    drive_timer = Timer(0.5, drive_timeout)
    drive_timer.start()

    return jsonify([])

@app.route("/actions/right", methods=["POST"])
def action_right():
    is_driving = True
    kit.continuous_servo[0].throttle = 0.5
    kit.continuous_servo[1].throttle = 0
    kit.servo[15].angle = 0
    msg_queue.put("right")
    drive_timer = Timer(0.5, drive_timeout)
    drive_timer.start()

    return jsonify([])

@app.route("/resting_throttle", methods=["GET"])
def get_resting_throttles():
    return jsonify({'0': resting_throttle[0], '1': resting_throttle[1]})

@app.route("/resting_throttle/<channel>", methods=["GET"])
def get_resting_throttle(channel):
    return jsonify({channel: resting_throttle[int(channel)]})
    
@app.route("/resting_throttle/<channel>/<value>", methods=["POST"])
def set_resting_throttle(channel, value):
    channel = int(channel)
    value = float(value)

    resting_throttle[channel] = value
    kit.continuous_servo[channel].throttle = resting_throttle[channel]

    return jsonify({'0': resting_throttle[0], '1': resting_throttle[1]})

def drive_timeout():
    is_driving = False
    kit.continuous_servo[0].throttle = resting_throttle[0]
    kit.continuous_servo[1].throttle = resting_throttle[1]
    kit.servo[15].angle = 180
    msg_queue.put("not driving")

@app.route('/infostream')
def info_stream():
    def the_stream():
        while True:
            yield "data: {}\n\n".format(msg_queue.get())
    return Response(the_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
