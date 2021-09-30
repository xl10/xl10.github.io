
# State
class State( object ):
	def  __init__(self):
		self.state = { }
		
	def hasVar(self, var):
		return self.state.has_key(str(var))
		
	def onion(self, var, value):
		self.state[str(var)] = value
		return self
		
	def value(self, var):
		if not self.state.has_key(var):
			error("Invalid reference to "+var)
		return self.state[var]
	
	def __str__(self):
		#print "State -- str"
		r = "{"
		sep = ""
		for v in self.state.keys():
			r += sep +"<" + v +", " + str(self.state[v]) +">"
			sep = ", "
		return r +"}"

	def __repr__(self):
		#print "State -- str"
		r = "{"
		sep = ''
		for v in self.state.keys():
			r += sep + "<" + v +", " + str(self.state[v]) +"> "
			sep = ", "	
		return r +"}"
