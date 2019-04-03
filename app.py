from flask import Flask, render_template, request, jsonify
from threading import Timer

app = Flask(__name__)
pins = { 1: {'state': True}, 42: {'state': False}}

is_driving = False

@app.route("/")
def main():
   # For each pin, read the pin state and store it in the pins dictionary:
   # Put the pin dictionary into the template data dictionary:
   templateData = {
      'pins' : pins
      }
   # Pass the template data into the template main.html and return it to the user
   return render_template('main.html', **templateData)

@app.route("/actions/<action>", methods=["POST"])
def take_action(action):
    print(action)
    if action == 'drive':
        if not is_driving:
            is_driving = True
            print("started driving")
            drive_timer = Timer(5, drive_timeout)
            drive_timer.start()

    return jsonify([])

def drive_timeout():
    is_driving = False
    print("stopped driving")

@app.route('/infostream')
def info_stream():
    def the_stream():
        while True:
            yield 'data: {}\n\n'.format(bla))
    return Response(the_stream(), mimetype="text/event-stream")

# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/pins/<changePin>/<action>")
def action(changePin, action):
   # Convert the pin from the URL into an integer:
   changePin = int(changePin)
   # Get the device name for the pin being changed:
   deviceName = "pin {}".format(changePin)
   print(pins)
   # If the action part of the URL is "on," execute the code indented below:
   if action == "on":
      # Set the pin high:
      # Save the status message to be passed into the template:
      message = "Turned " + deviceName + " on."
      pins[changePin]['state'] = True
   if action == "off":
      message = "Turned " + deviceName + " off."
      pins[changePin]['state'] = False

   # Along with the pin dictionary, put the message into the template data dictionary:
   templateData = {
      'pins' : pins
   }

   return render_template('main.html', **templateData)

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
