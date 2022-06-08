import struct

icmp_struct = "bbHHh"

class icmp():	

	def __init__(self, type=8, code=0, checksum=0, id=1, seq=1):
		self.type = type
		self.code = code
		self.checksum = checksum
		self.id = id
		self.seq = seq
		self.data = None
		self.raw = None
		self.pack()

	def pack(self):
		self.raw = struct.pack(icmp_struct,
			self.type,
			self.code,
			self.checksum,
			self.id,
			self.seq)

		self.checksum = self.checksum_calc(self.raw)

		self.raw = struct.pack(icmp_struct,
			self.type,
			self.code,
			self.checksum,
			self.id,
			self.seq)

	def checksum_calc(self, msg):

		s = 0       # Binary Sum

        # loop taking 2 characters at a time
		for i in range(0, len(msg), 2):

			a = msg[i]
			b = msg[i+1]
			s = s + (a+(b << 8))
            
        
		# One's Complement
		s = s + (s >> 16)
		s = ~s & 0xffff

		return s


if __name__ == "__main__":
	packet = icmp()