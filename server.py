import socket as sock
import sys
import os

EMPTY_LINE = "\r\n\r\n"
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
SEND_FILE_MSG = "HTTP/1.1 200 OK\r\n {0}".format(CONNECTION_SEPERATOR)
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


def filter(string, substr):
	return any(sub in string for sub in substr)


# check if need to open in binary or in regular read
def get_read_mode(file_name):
	list_of_binary_files = [".ico", ".jpg"]
	if filter(file_name, list_of_binary_files):
		return "rb"
	return 'r'


def send_file(socket, file_name, connection_method):
	# local search is from WORKSPACE = files
	mode = get_read_mode(file_name)
	file_local_path = os.path.join(WORKSPACE, file_name)
	with open(file_local_path, mode) as fin:
		file_content = fin.read()
		# len(file_content)
		msg = "{0}{1}\r\n Content-Length: {2}\r\n\r\n".format(SEND_FILE_MSG, connection_method,
					os.path.getsize(file_local_path))
	msg = msg.encode()
	msg += file_content if mode == "rb" else file_content.encode()
	socket.send(msg)


def handle_client(data, client_socket):
	# if you got no data - do nothing and close connection
	close_connection = True
	if not data:
		return close_connection
	# print the data from client
	print(data)

	file_name, connect_method = get_file_name_and_connection(data)
	# first check for redirect (because there is no file called like this)
	if file_name == REDIRECT:
		send_redirect_msg(client_socket)
		close_connection = True
	# if file not exists - send 404
	elif not is_file_exists(file_name):
		send_file_not_exists_error(client_socket)
		close_connection = True
	# else - there is a file with this name, sent it to client
	else:
		send_file(client_socket, file_name, connect_method)
		close_connection = False if connect_method == KEEP_CONNECTION else True
	return close_connection


def open_tcp_connection(port):
	# open tcp connection
	server = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
	server_ip = '0.0.0.0'
	server_port = int(port)
	server.bind((server_ip, server_port))
	server.listen()  # unlimited number of clients, will close connection via timeout or client request

	while True:  # iteration for every client
		client_socket, client_address = server.accept()
		client_socket.settimeout(1.0)
		while True:  # get one client commands until break
			try:
				data = ""
				while not data.endswith(EMPTY_LINE):  # get data until empty line
					data += client_socket.recv(1024).decode()
			except sock.timeout as e:
				# print(e)
				client_socket.close()
				break
			close_connection = handle_client(data, client_socket)
			if close_connection:
				client_socket.close()
				break


def error():
	raise TypeError('Error- invalid arguments')


if __name__ == '__main__':
	if len(sys.argv) != 2:
		error()
	else:
		open_tcp_connection(port=sys.argv[1])
