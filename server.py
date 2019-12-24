DEAFULT_FILE = "index.html"
CLOSE_CONNECTION = "close"
KEEP_CONNECTION = "keep-alive"
REDIRECT = "/redirect"
WORKSPACE = "./files"
VALID_REQUEST = "200 OK"
INVALID_REQUEST = "404 Not Found"
REDIRECT_REQUEST = "301 Moved Permanently"

# search timout for tcp recive socket
# directory of the files is in workspace/files

import socket as sock
import sys
import os

clients = []


class Client:
	def __init__(self, ip, port, files):
		self.ip = ip
		self.port = port
		self.files = files

	def __str__(self):
		return str(self.files)


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
	server_ip = '127.0.0.1'
	server_port = int(port)
	server.bind((server_ip, server_port))
	server.listen()  # unlimited number of clients, will close connection via timeout or client request
	while True:
		client_socket, client_address = server.accept()
		data = client_socket.recv(10240).decode()
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
