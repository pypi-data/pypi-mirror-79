class primes:
	
	def listprimes(start, end = None):
		L=[]
		if end == None:
			starting, ending = 2, start
		else:
			starting, ending = start, end
		if start < 2:
			return L
			
		for i in range(starting, ending+1):
			isprime = True
			
			for j in range(2, round(i**0.5)+1):
				if i % j == 0:
					isprime = False
					break
					
			if isprime:
				L.append(i)
				
		return L
	
	
	def isprime(nb):
		if nb < 2:
			return False
			
		for i in range(2,round(nb**0.5)+1):
			if nb % i == 0:
				return False
				
		return True




class math:

	def absolute(nb):
		return (-(nb*(nb<0)) + (nb*(nb>0)))
	
		
	def root(nb, root = 2):
		return (nb ** (1/root))




class logic:
	
	def logicand(c1, c2):
		return ((c1*c2) == 1)


	def logicnand(c1, c2):
		return ((c1+c2) == 0)
	
	
	def logicor(c1, c2):
		return ((c1+c2) >= 1)
	
	
	def logicnor(c1, c2):
		return((c1+c2) <= 1)
	

	def logicxor(c1, c2):
		return ((c1+c2)*(c1!=c2) == 1)
	
	
	def logicnot(c):
		return (c == 0)
	
	
	
	
class lists:
	
	def show(L, mode = "vertical"):
		if mode == "vertical":
			ending = "\n"
		elif mode == "horizontal":
			ending = " "
		else:
			ending = mode
		
		for i in L:
			print(i, end = ending)
