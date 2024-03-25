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

# Set the temp for the color baseline
base_temp = 85

sense = SenseHat()
sense.clear()

timestamp = datetime.now()

delay = 5

def get_sense_data():
    sense_data = []
    # Get environmental data
    sense_data.append(sense.get_temperature())
    sense_data.append((sense_data[0] * 1.8) + 32)
    sense_data.append(sense.get_pressure())
    sense_data.append(sense.get_humidity())

#    # Get colour sensor data (version 2 Sense HAT only)
#    red, green, blue, clear = sense.colour.colour
#    sense_data.append(red)
#    sense_data.append(green)
#    sense_data.append(blue)
#    sense_data.append(clear)
#
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

with open('data-' + timestr + '.csv', 'w', buffering=1, newline='') as f:
    data_writer = writer(f)
    data_writer.writerow(['temp_C', 'temp_F', 'pres', 'hum', 'datetime' ])

    while True:
        data = get_sense_data()
        led_temp_F = data[1]
        led_temp_F = str(round(led_temp_F, 1))

        actual_temp = data[1]

        if   actual_temp >= (base_temp + 3):
            RGB = [ 255, 0  ,   0 ]
        elif actual_temp >= (base_temp + 2):
            RGB = [ 255, 128,   0 ]
        elif actual_temp >= (base_temp + 1):
            RGB = [ 255, 255,   0 ]
        elif actual_temp >= (base_temp + 0): # <==== Start
            RGB = [ 255, 255, 255 ]
        elif actual_temp >= (base_temp - 1):
            RGB = [ 128, 255,   0 ]
        elif actual_temp >= (base_temp - 2):
            RGB = [ 0,   255,   0 ]
        elif actual_temp >= (base_temp - 3):
            RGB = [ 0,   255, 128 ]
        elif actual_temp >= (base_temp - 4):
            RGB = [ 0,   255, 255 ]
        elif actual_temp >= (base_temp - 5):
            RGB = [ 0,   0,   255 ]
        elif actual_temp >= (base_temp - 6):
            RGB = [ 0,   0,   150 ]
        elif actual_temp >= (base_temp - 7):
            RGB = [ 0,   0,   100 ]
        else:
            RGB = [ 255, 0,   255 ]

        print(base_temp,actual_temp)

        data[0]  = round(data[0], 5)
        data[1]  = round(data[1], 5)
        data[2]  = round(data[2], 5)
        data[3]  = round(data[3], 5)

        sense.show_message(led_temp_F, text_colour=RGB, scroll_speed=0.1)
        data.append(RGB)
        print(data)
        data_writer.writerow(data)
        time.sleep(5)

#    while True:
#        data = get_sense_data()
#        time_difference = data[-1] - timestamp
#        if time_difference.seconds > delay:
#            data_writer.writerow(data)
#            print(time_difference)
#            timestamp = datetime.now()