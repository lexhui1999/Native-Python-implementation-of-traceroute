import icmp_packet
import socket
import struct

packet = icmp_packet.icmp(id=12340)
dest_addr = "142.251.32.235"

def send_ping(packet, dest_addr, ttl):
	active_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
	active_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
	active_socket.sendto(packet.raw, (dest_addr, 1))

	return active_socket

def receive_ping(active_socket):
	packet_data, address = active_socket.recvfrom(2048)

	return packet_data, address

def unpack(packet_data, struct_format):
	unpacked_data = struct.unpack(struct_format, packet_data)

	return unpacked_data

if __name__ == "__main__":

	for i in range(30):
		packet = icmp_packet.icmp(id=100)
		current_socket = send_ping(packet, dest_addr, i+1)
		packet_data, address = receive_ping(current_socket)
		unpacked_data = unpack(packet_data[20:28], "!BBHHH")

		print(unpacked_data, address)
