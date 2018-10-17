from connection import  com


h = com()

print h.open()


print h.sensor.compressor_motor_temperature()


print h.sensor.compressor_supply_temperature()