import socket
import logging

class director:
	def __init__(self, server):
		self.server = server
		self.sock = None
		self.proxies = {}
		self.logger = logging.getLogger('dovesitter')

	def director_connect(self):
		handshake = "VERSION\tdirector-doveadm\t1\t0\n"
		try:
			self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
			self.sock.connect(self.server)
			self.sock.sendall(handshake)
			data = self.sock.recv(1024)
			if data == handshake:
				return True
			else:
				self.sock.close()
				return False
		except socket.error, msg:
			print msg
			self.logger.error('Problem connecting to director-doveadm. Verify if director is running: %s', msg,)
			return False

	def director_gethosts(self):
		if not self.director_connect():
			return {}
		self.sock.sendall('HOST-LIST\n')
		for line in self.sock.makefile('r'):
			if line == '\n':
				break
			host, weight, users = line.rstrip('\n').split('\t')
			self.proxies[host] = weight
		self.sock.close()
		return True

	def director_enablehost(self, host):
		if not self.director_connect():
			return False
		self.sock.sendall("HOST-SET\t" + host + "\t100\n");
		self.proxies[host] = '100'
		self.logger.info('Host %s enabled', host)
		self.sock.close()
		return True

	def director_disablehost(self, host):
		if not self.director_connect():
			return False
		self.sock.sendall("HOST-SET\t" + host + "\t0\n");
		self.sock.sendall("HOST-FLUSH\t" + host + "\n");
		self.proxies[host] = '0'
		self.logger.info('Host %s disabled', host)
		self.sock.close()
		return True
