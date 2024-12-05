def diag2(mat):
	N = len(mat)
	return set([mat[i][N-i-1]for i in range(N)])
def diag1(mat):
	N = len(mat)
	return set([mat[i][i]for i in range(N)])
def row(mat,k) :
	N = len(mat)
	return set([mat[k][i]for i in range(N)])
def col(mat,k) :
	N = len(mat)
	return set([mat[i][k]for i in range(N)])
class Board(list):
	def __init__(self,size:int):
		super().__init__([[None for i in range(size)] for i in range(size)])
	@property
	def len(self) :
		return len(self)
	def play(self,i:int,j:int , player ) :
		if self[i][j]: return False
		self[i][j] = player
		return True

	def check(self):
		for i in range(self.len) :
			if len(col(self,i)) == 1 and col(self,i) != {None}:
				return col(self,i).pop()
			if len(row(self,i)) == 1 and row(self,i) != {None}:
				return row(self,i).pop()
		if len(diag1(self)) == 1 and diag1(self) != {None} :
			return diag1(self).pop()
		if len(set(diag2(self))) == 1 and diag2(self) != {None} :
			return diag2(self).pop()
		return False
	#Used by HyperTTT.HyperGrid
	def _fill(self,player):
		for i in range(self.len):
			for j in range(self.len):
				self[i][j] = player

	def __repr__(self):
		s = ''
		for i, _ in enumerate(self):
			s+='\n|'
			for j , cell in enumerate(_) :
				s += f'{cell.value}|'
		
