import socket
import threading
import pickle

CLIENT_LIMIT = 20
MSG_LIMIT = 1024

A_inverse = [[4,-5,-2],[5,-6,-2],[-8,9,3]]
#clno=0
def decrypt(p):
        decrypt_text = []

        for k in range(len(p)):
            temp = []
            for l in range(len(p[0])):
                temp.append(0)
            decrypt_text.append(temp)

        for i in range(len(A_inverse)):
            for j in range(len(p[0])):
                for k in range(len(p)):
                    decrypt_text[i][j] += A_inverse[i][k] * p[k][j]

        return decrypt_text

def get_crc(dividend1,key):
    div=[]
    div[:0]=dividend1
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
    return div[kk:]

def get_char(decode_text):
    final_str=""
    row=len(decode_text)
    col=len(decode_text[0])

    for i in range(col):
        for j in range(row):
            val=decode_text[j][i]
            if val==27:
                final_str+=" "
            else:
                val+=64
                final_str += chr(val)
    return final_str

def convert_bin(msg,key_l):
    data = (''.join(format(ord(x), 'b') for x in msg))
    for i in range(1,key_l):
        data+= '0'
    return data

def server(clientsocket, address):

    while(True):
        msg = clientsocket.recv(MSG_LIMIT)
        print("-------------------------------------------------------------------------------")
        print("Recieved Message from transmitter")
        if msg=="exit":
            break

        cipher_text=pickle.loads(msg)
        crc=cipher_text[-1]
        crc_st=''.join(map(str,crc))
        cipher_text=cipher_text[:-1]

        decode_text=decrypt(cipher_text)
        print("Decoding Message")

        orignal=get_char(decode_text)

        #key_l=3
        #key = "1001"
        print("Caculating CRC")
        key="10001000000100001"
        key_l = len(key)
        dividend = convert_bin(orignal, key_l)
        crc_cal = get_crc(dividend, key)
        crc_cal_st=''.join(map(str,crc_cal))
        print("Message Recieved is:")
        print(orignal)

        if crc_st==crc_cal_st:
            print("Correct Message recieved")
        else:
            print("Wrong Message recieved")

    clientsocket.close()

#if( len(sys.argv) != 2):
#    print("Incorrect number of command line arguments. Pass IP and Port!")
#   exit()
ip="127.0.0.1"
port="9000"
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
serversocket.bind((ip, int(port)))
serversocket.listen(CLIENT_LIMIT)
while(True):
    (clientsocket, address) = serversocket.accept()
    print("Connected to",address)
    t1 = threading.Thread(target=server, args=(clientsocket, address,))
    t1.start()
serversocket.close()