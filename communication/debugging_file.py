from connection import  connection

h = connection()

print h.open()

print h.send_cmd('*rv\r')