# A robot that might someday do logo

![The robot](https://github.com/e8johan/roboten/raw/master/docs/images/roboten.jpeg)

This is the software part of a simple robot constructed from the following components:

* RaspberryPi ZeroW
* Adafruit Servo HAT
* Two 360 degrees servos with wheels
* An ordinary servo
* A dual port power bank
* A piece of wood

The software is build from the following components:

* Python
* Flask
* ServoKit

The code provides a web interface for the device where it can be controlled. It is based around a web page, plus a "REST" API where you can pass commands to the robot.

The commands include basic movement (left, right, forward, reverse, up and down), as well as calibration (resting_throttle). The system can also be told to shutdown cleany, and to upgrade (by doing a git pull).
