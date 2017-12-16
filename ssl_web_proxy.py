import SocketServer
import socket
import os, sys
import ssl

def CheckCONNECTMethod(data):
    if(data.split(' ')[0] == 'CONNECT'):
        return True
    return False

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        buf = self.request.recv(8192)
        
        if CheckCONNECTMethod(buf):
            #find host
            tmp = buf.split(' ')
            sockHost = tmp[1][0:tmp[1].find(':')] # until find :
            
            self.request.sendall('HTTP/1.1 Connection established\r\n\r\n')

            os.system('cd cert && _make_site.bat ' + hostname) # generate cert
            path = os.path.join(os.getcwd(),'cert',sockHost+'.pem')
            
            ssl_sock = ssl.wrap_socket(self.request, server_side = True, keyfile = path, cerfile = path) # wrap with cert
            
            ssl_request = ssl_sock.recv(8192) # get request

            try:
                sock = ssl.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
                sock.connect((sockHost, 443))

                sock.sendall(ssl_request) # send request

                while(1):
                    recvdata = sock.recv(8192)
                    if not recvdata:
                        break
                    #print(recvdata)
                    ssl_sock.sendall(data)

                sock.close()

            except socket.error:
                print("socket error")
                sock.close()
                sys.exit(1)

            ssl_sock.close()

if __name__ == '__main__':
    os.system('cd cert && _clear_site.bat') # clear cert
    os.system('cd cert && _init_site.bat') # init cert
    host, port = '127.0.0.1', 4433
    server = SocketServer.ThreadingTCPServer((host,port), MyTCPHandler)
    server.serve_forever()
