import time, socket, sys, pickle 
print('Client Server')

########################################################################
time.sleep(1)

#socket method
soc = socket.socket()
#get the hostname
chost = socket.gethostname()
#get the ip address
ip = socket.gethostbyname(chost)

#get the socket address from ip address
print(chost, '({})'.format(ip))
#We ask the client input the server ip address they want to connect to
# server_host = input('Enter server\'s IP address:')
server_host = '192.168.17.1'
#What is the clients name
name = input('Enter Clients name: ')
#the port
port = 1234
#connecting to the server
print('Trying to connect to the server: {}, ({})'.format(server_host, port))
#add a delay
time.sleep(1)

#connect to the server host through the port
soc.connect((server_host, port))
print("Connected...\n")

client_id = (soc.recv(1024)).decode()
soc.send(name.encode())

#receive the opening statement
opening = soc.recv(1024)
print(opening.decode())

###################################################################################
while True:

   confirmation = (soc.recv(1024)).decode() #before things begin we wait for confirmation
   print(confirmation)
   answer = input("Answer in (r/p/s): ")

   data = {'message_id': client_id, 'choice': answer} #message is put into pickle to send 2 data
   data = pickle.dumps(data) 
   soc.send(data)

   result = (soc.recv(1024)).decode() #we wait for the result
   print(result)					#print for the result
   break

