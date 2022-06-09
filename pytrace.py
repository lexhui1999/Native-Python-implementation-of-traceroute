import packets
import socket
import struct
import argparse


def is_ip(address):
    return address.replace('.', '').isnumeric()


def send_ping(packet, dest_addr, ttl):
    active_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
    active_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
    active_socket.sendto(packet.raw, (dest_addr, 1))

    return active_socket


def receive_ping(active_socket):
    active_socket.settimeout(1)
    packet_data, address = active_socket.recvfrom(2048)

    return packet_data, address


def unpack_icmp(packet_data, struct_format="!BBHHH"):
    unpacked_data = struct.unpack(struct_format, packet_data)

    return unpacked_data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("addr")
    parser.add_argument("-hop", help="Specify TTL (Time to live) on the IP packet.", type=int)
    args = parser.parse_args()
    dest_ip = None

    if is_ip(args.addr):
        dest_ip = args.addr
    else:
        try:
            dest_ip = socket.gethostbyname(args.addr)
        except socket.gaierror:
            print("Oops, hostname fails to resolve.")
            exit()
        except Exception as e:
            print(e.__class__)
            exit()

    for i in range(args.hop):
        packet = packets.ICMP_Packet(id=i + 1)
        current_socket = send_ping(packet, dest_ip, i + 1)
        try:
            packet_data, address = receive_ping(current_socket)
        except:
            print(i+1, "*")
            continue
        unpacked_data = unpack_icmp(packet_data[20:28])
        print(i+1, unpacked_data, address)
        if address[0] == dest_ip:
            print(f"Destination {dest_ip} reached in {i+1} hops")
            break


if __name__ == "__main__":
    main()
