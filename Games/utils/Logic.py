from abc import abstractmethod
class Validator:
	@abstractmethod
	def test(self,*x):
		pass
	def __call__(self,*x:object) -> bool:
		return self.test(*x)

class LogicValidator(Validator):
	def map(self,lst):
		pass

class NumericValidator(Validator):
	"""
		A version of Validator that cast input to float prior testing.
		They are also allowed to have multiple input and return.
	"""
	
	def __call__(self,*x:object):
		val = is_type(float)
		return self.test(*[val(i) for i in x])

class OR(LogicValidator):
	def __init__(self,*args : Validator):
		self.args = args
	def test(self,x : object) :
		return any([e(x) for e in self.args])
	def map(self,lst):
		n = len(self.args)
		return any([self.args[i//n](l) for i,l in enumerate(lst)])

class AND(LogicValidator):
	def __init__(self,*args : Validator):
		self.args = args
	def test(self,x : object) :
		return all([e(x) for e in self.args])
	def map(self,lst):
		n = len(self.args)
		return all([self.args[i//n](l) for i,l in enumerate(lst)])


class NOT(Validator):
	def __init__(self, a : Validator):
		self.args = a
	def test(self,x:object):
		return not(self.args(x))

class XOR(LogicValidator):
	def __new__(Validator,*args : Validator):
		return AND(OR(*args),NOT(AND(*args)))

class IN(Validator):
	def __init__(self,*a):
		self.args = set(a)
	def __call__(self,x) :
		return x in self.args

class contains(Validator):
	def __init__(self,a):
		self.args = a
	def __call__(self,x) :
		return self.args in x
class re_contains(Validator):
	def __init__(self,*a:str):
		self.args = a
		
	def __call__(self,x) :
		return any((re.search(a,x)for a in self.a))

class is_type(Validator):
	def __init__(self,t : type,cast : bool = True):
		self.t = t
		self.c = cast
	def __call__(self,x):
		if self.c : 
			try :	
				return self.t(x)
			except (ValueError, TypeError) as e: 
				return False
		return isinstance(x,self.t)


		
class above(NumericValidator):
	def __init__(self , m : float) :
		self.m = m
	def test(self,x) :
		return x > self.m
class bellow_equal(NumericValidator):
	def __new__(cls,m : float):
		return NOT(above(m))
class bellow(NumericValidator):
	def __init__(self , m : float) :
		self.m = m
	def test(self,x) :
		return x < self.m
class above_equal(NumericValidator):
	def __new__(cls,m : float):
		return NOT(bellow(m))
class in_between(NumericValidator):
	def __new__(cls,m : float,M : float):
		return AND(above(m),bellow(M))
class within(NumericValidator):
	def __new__(cls,m : float,M : float):
		return AND(above_equal(m),bellow_equal(M))

