import serial
import keyboard
import datetime
import threading
import time
import pandas as pd 

# Replace 'ttyACM0' with the appropriate serial port name
serial_port = '/dev/ttyACM0'

# Replace these settings with the appropriate baud rate and timeout
baud_rate = 9600
timeout = 1

# Initialize serial port
ser = serial.Serial(serial_port, baud_rate, timeout=timeout)

# Open a file to save the recorded data
output_file1 = 'keyData'
output_file2 = 'Accdata'

data_key = []
data_vibe = []

def read_serial():
    while True:
        data = ser.readline()
        if data:
            data_str = data.decode('utf-8').strip()
            x,y,z = data_str.split(",")
            current_time = datetime.datetime.now()
            # with open(output_file, 'a') as file:
            #     file.write(f"{current_time}\t{data_str}\t\n")  # Write timestamp, serial data, tab, and an empty column
            # print(current_time, data_str)
            #time.sleep(.1)
            data_vibe.append([str(current_time),float(x), float(y),float(z)])

def read_keyboard():
    while True:
        event = keyboard.read_event(suppress=True)
        if event.event_type == keyboard.KEY_DOWN:
            key = event.name
            current_time = datetime.datetime.now()
            data_key.append([str(current_time),key])
            
            # Wait for key release
            while True:
                event = keyboard.read_event(suppress=True)
                if event.event_type == keyboard.KEY_UP and event.name == key:
                    break

def write_out(file, data):
    df = pd.DataFrame(data)
    df.to_csv(f"{file}.csv", sep=",", index=False)
    # with open(output_file, 'a') as file:
    #     file.write(f"{data[0]},{}")  # Write timestamp, two tabs, and the key pressed
    #     print(current_time, key)


serial_thread = threading.Thread(target=read_serial)
keyboard_thread = threading.Thread(target=read_keyboard)

serial_thread.start()
keyboard_thread.start()

try:
    serial_thread.join()
    keyboard_thread.join()
except KeyboardInterrupt:
    write_out(output_file1, data_key)
    write_out(output_file2, data_vibe)
    print(data_key[0:4])
    #print(data_vibe[40:44])
    print("Recording stopped.")
finally:
    ser.close()
