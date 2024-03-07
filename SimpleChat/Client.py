from socket import *
s = socket(AF_INET,SOCK_STREAM)
host='127.0.0.1'
port= 40675
s.connect((host,port))

while True:
    client_message= input("client: ").encode()
    
    # Calculate the length of the message
    message_length = len(client_message)
    
    # Send the message in chunks if its size is larger than the buffer size
    if message_length > 2048:
        # Calculate the number of chunks needed
        num_chunks = message_length // 2048 + 1

        # Send each chunk iteratively
        for i in range(num_chunks):
            start_index = i * 2048
            end_index = min((i + 1) * 2048, message_length)
            s.send(client_message[start_index:end_index])

    else:
        # If message fits within buffer size, send it as is
        s.send(client_message)
    

    x=s.recv(2048)
    print("server:",x.decode())
    
    # To leve while loop write "end"
    if x.decode() == "end" :
         break
s.close()

