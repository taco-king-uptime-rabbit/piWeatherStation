#!/usr/bin/python3

#  https://projects.raspberrypi.org/en/projects/sense-hat-data-logger/1
#  https://www.pishop.us
#  https://www.rapidtables.com/web/color/RGB_Color.html
#    Raspberry Pi Sense HAT V2
#    Sense HAT (B) for Raspberry Pi (Waveshare)
#    Raspberry Pi Camera - 8 Megapixel (V2)

from sense_hat import SenseHat
from datetime import datetime
from csv import writer
import time
import os

DATA_DIR="/home/pi/Projects/piWeatherStation/output"

if not os.path.exists(DATA_DIR):
   os.makedirs(DATA_DIR)

sense = SenseHat()
sense.clear()

timestamp = datetime.now()

# how long between reads
delay = 0

# set color/light sensor 
#sense.color.gain = 1 
#sense.color.integration_cycles = 64

# Set the temp for the color baseline, convert C to F
starting_temp_C = round(sense.get_temperature(), 1)
starting_temp_F = (starting_temp_C * 1.8) + 32


def get_sense_data():
    sense_data = []
    # Get environmental data
    sense_data.append(starting_temp_F)
    sense_data.append(sense.get_temperature())
    sense_data.append((sense_data[1] * 1.8) + 32)
    sense_data.append(sense.get_pressure())
    sense_data.append(sense.get_humidity())

    # Get colour sensor data (version 2 Sense HAT only)
    red, green, blue, clear = sense.colour.colour
    sense_data.append(red)
    sense_data.append(green)
    sense_data.append(blue)
    sense_data.append(clear)

#    # Get orientation data
#    orientation = sense.get_orientation()
#    sense_data.append(orientation["yaw"])
#    sense_data.append(orientation["pitch"])
#    sense_data.append(orientation["roll"])
#
#    # Get compass data
#    mag = sense.get_compass_raw()
#    sense_data.append(mag["x"])
#    sense_data.append(mag["y"])
#    sense_data.append(mag["z"])
#
#    # Get accelerometer data
#    acc = sense.get_accelerometer_raw()
#    sense_data.append(acc["x"])
#    sense_data.append(acc["y"])
#    sense_data.append(acc["z"])
#
#    #Get gyroscope data
#    gyro = sense.get_gyroscope_raw()
#    sense_data.append(gyro["x"])
#    sense_data.append(gyro["y"])
#    sense_data.append(gyro["z"])

    # Get the date and time
    sense_data.append(datetime.now())

    return sense_data

timestr = time.strftime("%Y%m%d-%H%M%S")
DATA_FILE = DATA_DIR + '/' + 'data-' + timestr + '.csv'

with open(DATA_FILE, 'w', buffering=1, newline='') as f:
    data_writer = writer(f)
    data_writer.writerow(['starting_temp_F', 'temp_C', 'temp_F', 'pres', 'hum', 'Red', 'Green', 'Blue', 'Clear', 'datetime' ])

    while True:
        data = get_sense_data()
        led_temp_F = data[2]
        led_temp_F = str(round(led_temp_F, 1))

        actual_temp = data[2]

        if   actual_temp >= (starting_temp_F + 3):
            RGB = [ 255, 0  ,   0 ]
        elif actual_temp >= (starting_temp_F + 2):
            RGB = [ 255, 128,   0 ]
        elif actual_temp >= (starting_temp_F + 1):
            RGB = [ 255, 255,   0 ]
        elif actual_temp >= (starting_temp_F + 0): # <==== Start
            RGB = [ 255, 255, 255 ]
        elif actual_temp >= (starting_temp_F - 1):
            RGB = [ 128, 255,   0 ]
        elif actual_temp >= (starting_temp_F - 2):
            RGB = [ 0,   255,   0 ]
        elif actual_temp >= (starting_temp_F - 3):
            RGB = [ 0,   255, 128 ]
        elif actual_temp >= (starting_temp_F - 4):
            RGB = [ 0,   255, 255 ]
        elif actual_temp >= (starting_temp_F - 5):
            RGB = [ 0,   0,   255 ]
        elif actual_temp >= (starting_temp_F - 6):
            RGB = [ 0,   0,   150 ]
        elif actual_temp >= (starting_temp_F - 7):
            RGB = [ 0,   0,   100 ]
        else:
            RGB = [ 255, 0,   255 ]

        print(starting_temp_F,actual_temp)

        data[1]  = round(data[1], 5)
        data[2]  = round(data[2], 5)
        data[3]  = round(data[3], 5)
        data[4]  = round(data[4], 5)

        sense.show_message(led_temp_F, text_colour=RGB, scroll_speed=0.08)
        data.append(RGB)
        print(data)
        data_writer.writerow(data)
        time.sleep(delay)

#    while True:
#        data = get_sense_data()
#        time_difference = data[-1] - timestamp
#        if time_difference.seconds > delay:
#            data_writer.writerow(data)
#            print(time_difference)
#            timestamp = datetime.now()
