#Manage memory space for constants
#Return Address = 0; Can either be 4 byte data or 4 byte pointer
#Arguments = 1,2,3; 
class StaticMemory:
	mem = [0, 1, -1, 0, 0, 0] # Reserve space for the stack pointer, const 1/-1, and funciton args
	def malloc(self, size):
		baseIndex = len(self.mem);
		for i in range(0,size):
			self.mem.append(0)
		return baseIndex
	
	def set(self, base, value):
		self.mem[base] = value;	

	def get(self, base):
		return self.mem[base]
	
	def toString(self):
		res = ""
		for i,val in enumerate(self.mem):
			res += str(val) + "\n"
		return res

class DynamicMemory:
	mem = []
	def malloc(self, size):
		baseIndex = len(mem);
		for i in range(0,size):
			mem.append(0)
		return baseIndex
	def dealloc(self, base, size):
		return
	def set(self, base, value):
		return "SET"