import socket
s = socket.socket()
host = socket.gethostname()
#print(host)
port = 9898
#tumple degistirelemez liste
s.bind((host,port))

# 5 tane conn que ya atip bekletebiliyor
s.listen(30)

while True:
    # baglanti kurulduktan sonra atanan connection degiskenleri iki tane donuyor
    c,addr = s.accept()
    print('Connection from', addr)
    c.send('Thank you for connecting')
    c.close()