import socket
import ssl
import re

HOST_IP = socket.gethostbyname('project1.5700.network')
T_PORT = 27995
BUFF_SIZE = 16384

# establish TSL connection
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_wrap_socket = ssl.wrap_socket(my_socket, ssl_version=ssl.PROTOCOL_TLSv1)
my_wrap_socket.connect((HOST_IP, T_PORT))

INITIAL_MESSAGE = 'cs5700spring2022 HELLO nguyen.bac\n'
ERROR_MESSAGE = "cs5700spring2022 ERR #DIV/0\n"

my_wrap_socket.send(INITIAL_MESSAGE.encode())


def modify_server_response(response_from_server):
    modified_response = re.sub("<<", "<< 13", response_from_server[22:])
    return modified_response


def return_to_response(modified_response):
    try:
        evaluate_result = eval(modified_response)
        return_to_server = "cs5700spring2022 STATUS " + str(evaluate_result) + "\n"
        return return_to_server.encode()
    except ZeroDivisionError:
        return ERROR_MESSAGE.encode()


def get_server_response():
    response_from_server = ""
    while True:
        data_from_server = my_wrap_socket.recv(BUFF_SIZE).decode()
        response_from_server += data_from_server
        if data_from_server[-1] == "\n":
            break
    return response_from_server


while True:
    response_from_server = get_server_response()
    if response_from_server[17:20] == "BYE":
        #print(response_from_server)
        my_wrap_socket.close()
        break
    modified_response = modify_server_response(response_from_server)
    response_from_client = return_to_response(modified_response)
    #print(response_from_client.decode())
    my_wrap_socket.send(response_from_client)





