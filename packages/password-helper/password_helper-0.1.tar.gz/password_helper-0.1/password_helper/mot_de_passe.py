from random import *
import pandas as pd
class Pwd_helper():
	def __init__(self, phrase):
		self.phrase = phrase
		self.pwd = ''
		data = {1:' d, t', 2:' n', 3:' m', 4:' r', 5:' l', 6:' j, sh, ch',
			7:' k, g', 8:' f, v', 9:' b, p', 0:' s, x, z, th'}
		self.phonetic = pd.DataFrame.from_dict(data, orient='index', columns=['letter'])
        
	def make_alphanum(self):
		
		vowel = ['a', 'e', 'i', 'o', 'u', 'y', 'w', 'h', ',', '.']
		
		mnemo = {'b': 9, 'c': 7, 'd': 1,'f': 8, 'g': 7, 'j': 6, 'k': 7, 'l': 5, 'm': 3,
	 		'n': 2, 'p': 9,'q': 7,'r': 4,'s': 0,'t': 1,'v': 8,'x': 0,'z': 0}
		
		#prepare string
		self.phrase=self.phrase.lower()
		self.phrase = self.phrase.replace(' ', '')
		for v in vowel:
			self.phrase = self.phrase.replace(v,'')

		# convert to alphanumeric
		text = self.phrase

		#n = len(text)
		k = ''
		for i in range (0, len(text)):
			r = randint(i, i+2)
			if r == i:
				sub = mnemo[text[i]]
				k = k + str(sub)
			else:
				k = k + text[i]
		return k
