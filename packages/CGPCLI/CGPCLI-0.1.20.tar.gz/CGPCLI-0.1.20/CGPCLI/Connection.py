import socket

from CGPCLI.Errors import FailedLogin, ConnectionTimeOut

def connect(host, port=106):
    '''Create a connection with CGP server via socket
    
    :host str
    :port int
    :rtype socket
    
    '''
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        sock.settimeout(5.0)
        
        read(sock)
        
        return sock
    except socket.error as e:
        raise e

def login(sock, username, pwd):
    '''Log in CGP Account. Raises an Exception on fail login
    
    :sock socket
    :username str
    :pwd str
    
    '''
    
    check = '515'
    while check != '200':
        sock.send((f'USER {username}\n').encode())
        check = read(sock)            

        sock.send((f'PASS {pwd}\n').encode())
        check = read(sock, get=True)['header'][:3]
        
        if check == '515':
            raise FailedLogin()

def disconnect(sock):
    '''Log in CGP Account
    
    :sock socket
    
    '''
    try:
        sock.send(('QUIT\n').encode())
    except ConnectionAbortedError:
        pass
    
    sock.close()

def read(sock, get=False, data=False):
    '''Metod that reads messages from server and returns dict containing server response
    if get parameter is set to True.
    
    Return examples:
    {"header": "200, "body": "OK"}
    {"header": "200", "body": "data follow"}
    
    :sock socket
    :get bool
    :rtype dict
    
    '''
    
    message = {}

    if not data:
        msg = sock.recv(4).decode()
        message['header'] = msg.strip()

    full = ''
    while True:
        try:
            msg = sock.recv(4096)
            full += msg.decode()
            
            if full[-2:] == '\r\n':
                message['body'] = full[:-2]
                break

        except ConnectionAbortedError:
            disconnect(sock)
            raise ConnectionTimeOut()

        except socket.timeout:
            break

    if 'get':
        return message       