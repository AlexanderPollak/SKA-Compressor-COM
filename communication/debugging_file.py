from connection import  com
from connection import sensor

h = com()

print h.open()

print h.sensor.contr_temperature()

