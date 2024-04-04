from socket import *
s = socket(AF_INET,SOCK_STREAM)
host='127.0.0.1'
port= 6500
s.connect((host,port))
print("if you want to terminate the session write 'end' ")

while True:
    client_message= input("client: ").encode('utf-8')
    
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
    
    # To leve while loop write "end"
    if client_message.decode('utf-8') == "end" :
         break
    
    x=s.recv(2048)
    print("server:",x.decode('utf-8'))

    
s.close()
