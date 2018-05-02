
import time
import serial



s = serial.Serial('/dev/ttyACM0')

N = 10
for i in xrange(N):
    s.write("STATUS\0")
    print(s.readline())
    print(s.readline())
    #time.sleep(0.5)
