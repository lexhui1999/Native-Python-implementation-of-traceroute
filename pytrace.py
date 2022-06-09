import packets
import socket
import struct
import argparse

packet = packets.icmp(id=12340)
dest_addr = "8.8.8.8"

def is_ip(address):
    return address.replace('.', '').isnumeric()

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

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("addr")
	parser.add_argument("-hop", help="Specify TTL (Time to live) on the IP packet.", type=int)
	args = parser.parse_args()

	if is_ip(args.addr):
		dest_addr = args.address
	else:
		try:
			dest_addr = socket.gethostbyname(args.addr)
		except socket.gaierror:
			print("Oops, hostname fails to resolve.")
			exit()
		except Exception as e:
			print(e._class__)
			exit()

	for i in range(args.hop):
		packet = packets.icmp(id=100)
		current_socket = send_ping(packet, dest_addr, i+1)
		packet_data, address = receive_ping(current_socket)
		unpacked_data = unpack(packet_data[20:28], "!BBHHH")

		print(i+1, unpacked_data, address)


if __name__ == "__main__":

	main()
