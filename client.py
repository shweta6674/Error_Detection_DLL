import socket
import threading
import pickle
#import numpy

# Global constants
CLIENT_LIMIT = 20
MSG_LIMIT = 1024

A=[[0,-3,-2],[1,-4,-2],[-3,4,1]]
A_inverse=[[4,-5,-2],[5,-6,-2],[-8,9,3]]

def get_num(text):
    encrypt_num=[]
    for i in text:
        char = i.upper()
        #print(char)
        # Cast chr to int and subtract 65 to get 0-25
        if char == " ":
            integer = 27
        else:
            integer = ord(char) - 64
        encrypt_num.append(integer)

    val = len(encrypt_num) % 3
    if val == 1:
        encrypt_num.append(27)
        encrypt_num.append(27)
    if val == 2:
        encrypt_num.append(27)

    return encrypt_num

def create_matrix(encrypt_num,m,n):
    finalp=[]
    #print(finalp)
    k=0

    for i in range(0, m):
        temp=[]
        finalp.append(temp)

    for i in range(0,n):
        for j in range(0,m):
             """print("{j}:{i}:={encrypt_num[k]}")
             print(str(j)+":"+str(i)+"="+str(encrypt_num[k]))"""
             finalp[j].append(encrypt_num[k])
             k+=1
    return finalp

def multiply(A,p,op1):
    cipher_text=[]

    for k in range(len(p)):
        temp=[]
        for l in range(len(p[0])):
            temp.append(0)
        cipher_text.append(temp)

    for i in range(len(A)):
        for j in range(len(p[0])):
            for k in range(len(p)):
                cipher_text[i][j]+=A[i][k]*p[k][j]
    if op1=='n':
      if len(A)>2 and len(p[0])>3:
        cipher_text[2][3]+=1
        cipher_text[len(A)-1][len(p[0])-1] += 10

    return cipher_text

def convert_bin(msg,key_l):
    msg=msg.upper()
    data = (''.join(format(ord(x), 'b') for x in msg))
    #print(data)
    for i in range(1,key_l):
        data+= '0'
    return data

def get_crc(dividend,key):
    div=[]
    div[:0]=dividend
    dl=len(div)
    n=len(key)
    i=0
    while i<=dl-n:
        for  j in range(0,n):
            if div[i+j]==key[j]:
                div[i + j]='0'
            else:
                div[i + j] = '1'
        while i<dl and div[i]!='1':
            i+=1
    kk=-(n-1)
    #print(div)
    #print(div[kk:])
    return div[kk:]

def client_main(server_ip, server_port):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((server_ip, int(server_port)))
    while(True):
        msg = input(">>")
        print("----------------------------------------------------------------------------------")
        print("Message to be transmitted")
        print (msg.upper())
        val = len(msg) % 3
        if val == 1:
            msg += " " + " "
        if val == 2:
            msg += " "

        # convert msg to binary for crc
        # key = "1001"
        key = "10001000000100001"
        key_l = len(key)
        dividend = convert_bin(msg, key_l)
        crc = get_crc(dividend, key)
        print("Calculated Message CRC")
        print("As a transmitter want to send correct message? Y/N?")
        t=input()
        op=t.lower()
        #Encoding msg
        print("Encoding Message")
        encrypt_num = get_num(msg)
        m=3
        n=len(encrypt_num)/3
        p= create_matrix(encrypt_num,m,n)
        cipher_text=multiply(A,p,op)
        # Exit
        if(msg=="exit"):
            clientsocket.send(msg.encode())
            break
        cipher_text.append(crc)
        send=pickle.dumps(cipher_text)
        clientsocket.send(send)
        print("Message sent")
        #msg = clientsocket.recv(MSG_LIMIT).decode()

    clientsocket.close()


"""if( len(sys.argv) != 2):
    print("Incorrect number of command line arguments. Pass IP and Port!")
    exit()"""
server_ip="127.0.0.1"
server_port="9000"
#client_ip, client_port = sys.argv[2].split(':')

t1 = threading.Thread(target=client_main, args=(server_ip, server_port))
t1.start()

