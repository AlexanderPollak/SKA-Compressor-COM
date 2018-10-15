from connection import  com
from connection import sensor

h = com()

print h.open()

print h.sensor.compressor_motor_temperature()

print h.compressor.disable()

print h.compressor.enable()