# Native-Python-implementation-of-traceroute

This project implements the traceroute functionality in native Python. Traceroute is a popular network diagnostic tool used to record and determine hops along a certain route from one host to another, through the internet. Traceroute works by manupulating the TTL on ICMP packets so that the packets would get sent back from every host along the route until the destination is reached. By examining the ICMP packets that got sent back, the IP address of the hops can be determined. The ICMP packets in this project are created from scratch.

To use this project. simply run pytrace.py with two arguments:

1. Domain name or ip address, without flag
2. Max TTL, with flag -hop

Example: ```sudo python3 pytrace.py google.com -hop 30```

You will need sudo privileges to run this on Linux due to socket creation.
