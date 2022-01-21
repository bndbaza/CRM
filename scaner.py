import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
print(ser.name)
line = ser.readline()
print(line)