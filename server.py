# search timout for tcp recive socket
# directory of the files is in workspace/files
# TODO: understand how read data, when to finish, ("\r\n\r\n")
# TODO: check if after redirection, what to do.
# TODO: what is the seperator of new line
# TODO: what is new empty line
import socket as sock
import sys
import os

DEFAULT_FILE = "index.html"
DEFAULT_REPRESENTATION = "/"
CLOSE_CONNECTION = "close"
KEEP_CONNECTION = "keep-alive"
REDIRECT = "redirect"
WORKSPACE = "files"
VALID_REQUEST = "200 OK"
CONNECTION_SEPERATOR = "Connection: "
RESULT_FILE_PATH = "/result.html"
FILE_NOT_FOUND_MSG = "HTTP/1.1 404 Not Found\r\n {0}{1}".format(CONNECTION_SEPERATOR, CLOSE_CONNECTION)
REDIRECT_MSG = "HTTP/1.1 301 Moved Permanently\r\n {0}{1}\r\nLocation: {2}\r\n\r\n".format(CONNECTION_SEPERATOR,
                                                                                           CLOSE_CONNECTION,
                                                                                           RESULT_FILE_PATH)


def get_file_name_and_connection(data):
	data_parsed = data.split("\r\n")
	first_row = data_parsed[0]
	file_name = first_row.split(" ")[1]
	connect_method = ""
	# convert to default if neccesery. o.w remove first '/'
	file_name = DEFAULT_FILE if file_name == DEFAULT_REPRESENTATION else file_name[1:]
	for row in data_parsed:
		if row.startswith(CONNECTION_SEPERATOR):
			connect_method = row.split(CONNECTION_SEPERATOR)[1]
			break
	return file_name, connect_method


def is_file_exists(file_path):
	# local search is from WORKSPACE = files
	file_local_path = os.path.join(WORKSPACE, file_path)
	return os.path.isfile(file_local_path)


def send_redirect_msg(socket):
	socket.send(REDIRECT_MSG.encode())


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


def send_file(socket, file_name):
	pass


def handle_client(data, client_socket):
	file_name, connect_method = get_file_name_and_connection(data)
	if not is_file_exists(file_name):
		send_file_not_exists_error(client_socket)
	elif file_name == REDIRECT:
		send_redirect_msg(client_socket)
	else:
		send_file(client_socket, file_name)


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
		handle_client(data, client_socket)
		client_socket.close()
		break


if __name__ == '__main__':
	if len(sys.argv) != 2:
		error()
	else:
		open_tcp_connection(port=sys.argv[1])
