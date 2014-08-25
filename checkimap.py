import threading
import logging
import logging.config
import time
import socket
import director
import sys
from struct import *
import fcntl

class checkimap(threading.Thread):
	def __init__(self, host_port, director):
		threading.Thread.__init__(self)
		self.kill_received = False
		self.logger = logging.getLogger('dovesitter')
		self.myip = socket.gethostbyname(socket.gethostname())
		self.host_port = host_port
		self.director = director

	def run(self):
		self.logger.info('CheckImap thread started')
		self.director.director_gethosts()
		while not self.kill_received:
			if not self.director.proxies: self.kill_received = True
			for i in self.director.proxies.keys():
				result = self.proxy_test(i)
				if result == True and self.director.proxies[i] == '0':
					self.logger.info('Server %s is ok.',i)
					self.director.director_enablehost(i)
				elif result == False and self.director.proxies[i] == '100':
					self.logger.warning('Server %s is not ok.',i)
					self.director.director_disablehost(i)
			time.sleep(2)

	def checksum(self, msg):
		s = 0
		for i in range(0, len(msg), 2):
			w = (ord(msg[i]) << 8) + (ord(msg[i+1]) )
			s = s + w
                
		s = (s>>16) + (s & 0xffff);
		s = ~s & 0xffff
		return s

	def proxy_test(self, host):
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
		except socket.error , msg:
			sys.exit()

		s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

		packet = '';
		source_ip = self.myip
		dest_ip = host
		dest_port = int(self.host_port)
		ihl = 5
		version = 4
		tos = 0
		tot_len = 20 + 20
		id = 54321
		frag_off = 0
		ttl = 255
		protocol = socket.IPPROTO_TCP
		check = 10
		saddr = socket.inet_aton(source_ip)
		daddr = socket.inet_aton(dest_ip)
		ihl_version = (version << 4) + ihl

		ip_header = pack('!BBHHHBBH4s4s', ihl_version, tos, tot_len, id, frag_off, ttl, protocol, check, saddr, daddr)

		source = 1234
		dest = dest_port
		seq = 0
		ack_seq = 0
		doff = 5
		fin = 0
		syn = 1
		rst = 0
		psh = 0
		ack = 0
		urg = 0
		window = socket.htons(5840)
		check = 0
		urg_ptr = 0

		offset_res = (doff << 4) + 0
		tcp_flags = fin + (syn << 1) + (rst << 2) + (psh <<3) + (ack << 4) + (urg << 5)

		tcp_header = pack('!HHLLBBHHH', source, dest, seq, ack_seq, offset_res, tcp_flags, window, check, urg_ptr)

		source_address = socket.inet_aton(source_ip)
		dest_address = socket.inet_aton(dest_ip)
		placeholder = 0
		protocol = socket.IPPROTO_TCP
		tcp_length = len(tcp_header)

		psh = pack('!4s4sBBH', source_address, dest_address, placeholder, protocol, tcp_length);
		psh = psh + tcp_header;

		tcp_checksum = self.checksum(psh)

		tcp_header = pack('!HHLLBBHHH', source, dest, seq, ack_seq, offset_res, tcp_flags, window, tcp_checksum, urg_ptr)

		packet = ip_header + tcp_header

		s.sendto(packet, (dest_ip ,0 ))

		count = 10

		while count:
			packet = s.recvfrom(68)

			packet = packet[0]

			ip_header = packet[0:20]
 
			iph = unpack('!BBHHHBBH4s4s', ip_header)
 
			version_ihl = iph[0]
			version = version_ihl >> 4
			ihl = version_ihl & 0xF
 
			iph_length = ihl * 4
 
			ttl = iph[5]
			protocol = iph[6]
			s_addr = socket.inet_ntoa(iph[8]);
			d_addr = socket.inet_ntoa(iph[9]);
 
			tcp_header = packet[iph_length:iph_length+20]
 
			tcph = unpack('!HHLLBBHHH', tcp_header)

			if str(d_addr) == source_ip:
				if str(tcph[0]) == str(dest_port) and tcph[5] == 0x12:
					return True
			count = count - 1
		return False
