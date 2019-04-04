from flask import Flask, render_template, request, jsonify, Response
from threading import Timer
from queue import Queue

app = Flask(__name__)

is_driving = False
msg_queue = Queue()

@app.route("/")
def main():
   templateData = {}
   return render_template('main.html', **templateData)

@app.route("/actions/<action>", methods=["POST"])
def take_action(action):
    if action == 'drive':
#        if not is_driving:
            is_driving = True
            msg_queue.put("driving")
            drive_timer = Timer(5, drive_timeout)
            drive_timer.start()

    return jsonify([])

def drive_timeout():
    is_driving = False
    msg_queue.put("not driving")

@app.route('/infostream')
def info_stream():
    def the_stream():
        while True:
            yield "data: {}\n\n".format(msg_queue.get())
    return Response(the_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
