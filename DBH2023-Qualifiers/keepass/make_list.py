password='deutschlands00_00B3ST3R00_00Hack3r2023'
second_char=['3','N','c','d','e','f','g','-','#','W','X','C','0',';']
first_char=[chr(i) for i in range(32,128)]

wordlist=[]
for s in second_char:
	for f in first_char:
		wordlist+=[f+s+password]

with open('wordlist.txt','w') as f:
	for word in wordlist:
		f.write(word+'\n')
