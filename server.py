# search timout for tcp recive socket
# directory of the files is in workspace/files
# TODO: understand how read data, when to finish, ("\r\n\r\n")
import socket as sock
import sys
import os

DEFAULT_FILE = "index.html"
DEFAULT_REPRESENTATION = "/"
CLOSE_CONNECTION = "close"
KEEP_CONNECTION = "keep-alive"
REDIRECT = "/redirect"
WORKSPACE = "files"
VALID_REQUEST = "200 OK"
INVALID_REQUEST = "404 Not Found"
REDIRECT_REQUEST = "301 Moved Permanently"
CONNECTION_SEPERATOR = "Connection: "
FILE_NOT_FOUND_MSG = "HTTP/1.1 {0}\r\n {1}{2}".format(INVALID_REQUEST, CONNECTION_SEPERATOR, CLOSE_CONNECTION)


def parse_data(data):
	data_parsed = data.split("\r\n")
	first_row = data_parsed[0]
	file_name = first_row.split(" ")[1]
	connect_method = ""
	# convert to default if neccesery:
	if file_name == DEFAULT_REPRESENTATION:
		file_name = DEFAULT_FILE
	for row in data_parsed:
		if row.startswith(CONNECTION_SEPERATOR):
			connect_method = row.split(CONNECTION_SEPERATOR)[1]
			break
	return file_name, connect_method


def is_file_exists(file_path):
	# local search is from WORKSPACE = files
	file_local_path = os.path.join(WORKSPACE, file_path)
	return os.path.isfile(file_local_path)


def send_file_not_exists_error(socket):
	socket.send(FILE_NOT_FOUND_MSG.encode())
	# TODO: check if need to close the socket.


def error():
	raise TypeError('Error- invalid arguments')


def is_valid_input(splited_data):
	list_length = len(splited_data)
	if list_length < 2:
		return False
	choice = splited_data[0]
	if choice not in ['1', '2']:
		return False
	choice = int(choice)
	if choice == 1 and list_length != 3:
		return False
	if choice == 2 and list_length != 2:
		return False
	return True


def search_files_contains(substring_to_find):
	files_msg = ""
	for client in clients:
		for file in client.files:
			if substring_to_find in file:
				files_msg += "{0} {1} {2},".format(file, client.ip, str(client.port))
	if files_msg:
		files_msg = files_msg[:-1] + '\n'  # remove the last ',' and add '\n
	return files_msg


def send_files_list(file_name, socket):
	files_msg = search_files_contains(file_name)
	socket.send(files_msg.encode())


def add_files_to_client(ip, port, files_list):
	for client in clients:
		if client.ip == ip and client.port == port:
			client.files += files_list
			return
	# if new client
	new_client = Client(ip, port, files_list)
	clients.append(new_client)


def add_client(port, files, ip):
	# port need to be a number
	if not port.isdigit():
		return
	# make list of files
	files_list = files.split(',')

	# if client exists, add files to it's file, else create new client.
	for client in clients:
		if client.ip == ip and client.port == port:
			client.files += files_list
			return
	# if new client
	new_client = Client(ip, port, files_list)
	clients.append(new_client)


def handle_client(client_data, ip, socket):
	splited_data = client_data.split(" ")
	if not is_valid_input(splited_data):
		return
	choice = int(splited_data[0])
	if choice == 1:
		add_client(splited_data[1], splited_data[2], ip)
	if choice == 2:
		send_files_list(splited_data[1], socket)


def open_tcp_connection(port):
	# open tcp connection
	server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
	server_ip = '0.0.0.0'
	server_port = int(port)
	server.bind((server_ip, server_port))
	server.listen()  # unlimited number of clients, will close connection via timeout or client request
	while True:
		client_socket, client_address = server.accept()
		data = client_socket.recv(2500).decode()
		client_ip = client_address[0]
		# handle_client(data.decode(), client_ip, client_socket)
		print(data)
		client_socket.close()
		break


if __name__ == '__main__':
	if len(sys.argv) != 2:
		error()
	else:
		open_tcp_connection(port=sys.argv[1])
