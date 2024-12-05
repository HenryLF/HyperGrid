from PIL import Image
from os import listdir
import io
import base64
import sys

S = 'icon = {'

if len(sys.argv) == 0 :
	for file_name in listdir() :
		if file_name.split('.')[-1] != 'png' : continue
		S += f'"{file_name.replace(".png","")}" : '
		with open(file_name,'rb') as f :
			 s = base64.b64encode(f.read())
		S += f'{s},\n'
else :
	for file_name in sys.argv :
		if file_name.split('.')[-1] != 'png' : continue
		S += f'"{file_name.replace(".png","")}" : '
		with open(file_name,'rb') as f :
			 s = base64.b64encode(f.read())
		S += f'{s},\n'

S+= '}'
with open('icon_b64.py','w') as f :
	f.write(S)
