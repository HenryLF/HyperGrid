import matplotlib.pyplot as plt
import numpy as np
from itertools import product
def closestDivisors(n):
	a = round(np.sqrt(n))
	while n%a > 0: a -= 1
	return a,n//a
#for i in range(7,20 ):
#	x = range(0,255,i)
#	rgb = np.array([(i[0]/254,i[1]/254,i[2]/254) for i in product(x,x,x)])

#	print(i,rgb.shape,closestDivisors(rgb.shape[0]))
#	rgb = rgb.reshape(*closestDivisors(rgb.shape[0]),3)
x = range(0,255,11)
rgb = np.array([(255,255,255) for i in product(x,x,x)])
print(rgb.shape,closestDivisors(rgb.shape[0]))
rgb = rgb.reshape(*closestDivisors(rgb.shape[0]),3)

plt.figure()
plt.imshow(rgb)
plt.show()
