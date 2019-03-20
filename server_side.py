#first we import the necessary libraries
import time, socket, sys, pickle

#function for comparing
#True means the first client was the winner, False the opposite
#for draw we use simple equality comparison outside the function
def compare(c1_Choice,c2_Choice):
   results = {('p','r') : True,
              ('p','s') : False,
              ('r','p') : False,
              ('r','s') : True,
              ('s','p') : True,
              ('s','r') : False}
   winner = results[(c1_Choice,c2_Choice)]
   return winner

########################################################################################
#delay
time.sleep(1)

#the socket method
soc = socket.socket()

#get the hostname from the socket
host_name = socket.gethostname()

#get the ip from the socket
ip = socket.gethostbyname(host_name)

port = 1234 #setting the port for connection

########################################################################################

#first we need to bind the hostname with the port
soc.bind ((host_name, port))
print(host_name, '({})'.format(ip))
#input server name
# sv_name = input('Enter server name: ')

#Here we have the lists for clients connection and choices
clients = []
client_choices = ['r', 'r'] 

########################################################################################

for i in range(2): #we will listen twice for connections
   soc.listen()
   print('Waiting for connections..')
   connection, addr = soc.accept() 
   
   clients.append(connection) #connection data will be saved to the list to check
   print('Received connection from', addr[0], '(', addr[1], ')\n')
   print('Connection Established. Connected from: {}, ({})'.format(addr[0], addr[0]))

   #get a connection from client side
   connection.send(str(i).encode()) #inform client of their id
   client_name = (connection.recv(1024)).decode()

   print('%s has connected.' % (client_name)) 
   connection.send(("""
      \nWELCOME TO THE ROCK p SCISSORS GAME\n\n
Please choose your weapon of choice rock, p, or scissor (r/p/s)\n
(result will appear after 2nd client has answered)\n""").encode())

# print("LET US BEGIN THE ROCK p SCISSORS SHOWDOWN")

#######################################################################################

while True:
   #we will first ask the 1st client what their answer is
   #then after saving their answer and id we will proceed to ask the 2nd client
   #message id is used to ensure the clients identity
   for x in range(2):
      clients[x].send(("Please send you answer now").encode())
      data = clients[x].recv(1024)
      if not data:
         break
      data = pickle.loads(data)

      print("Client: {message_id}, data: {choice}".format(**data))
      the_id = int('{message_id}'.format(**data))
      choice = '{choice}'.format(**data)
      client_choices[the_id] = choice

   # print(client_choices)
   print("showdown.....")

#We determine the winner
   if(client_choices[0] == client_choices[1]):
      result = "IT IS A DRAW"
      clients[0].send((result).encode())
      clients[1].send((result).encode())
      break      

   else:   
      result = compare(client_choices[0], client_choices[1])
      if(result == True):
         clients[0].send(("WINNER WINNER CHICKEN DINNER!").encode())
         clients[1].send(("LOSER!!!!").encode())
      else:
         clients[1].send(("WINNER WINNER CHICKEN DINNER!").encode())
         clients[0].send(("LOSER!!!!").encode())
      break




