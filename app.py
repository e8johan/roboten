from flask import Flask, render_template, request, jsonify, Response
from threading import Timer
from queue import Queue

app = Flask(__name__)

is_driving = False
msg_queue = Queue()

@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   # Put the pin dictionary into the template data dictionary:
   templateData = {}
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

@app.route("/actions/<action>", methods=["POST"])
def take_action(action):
    if action == 'drive':
#        if not is_driving:
            is_driving = True
            msg_queue.put("driving")
            print("started driving")
            drive_timer = Timer(5, drive_timeout)
            drive_timer.start()

    return jsonify([])

def drive_timeout():
    is_driving = False
    msg_queue.put("not driving")
    print("stopped driving")

@app.route('/infostream')
def info_stream():
    print("someone requested the stream")
    def the_stream():
        while True:
            print("something to yield")
            yield "data: {}\n\n".format(msg_queue.get())
    return Response(the_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
