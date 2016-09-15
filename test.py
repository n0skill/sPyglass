lst = []

lst.append('123456789')
lst.append('121212121')
lst.append('blbl2131231')

for i, s in enumerate(lst):
	if len(s) > 4:
		lst.insert(i+1, s[0:int(len(s)/2)])
		lst.insert(i+2, s[int(len(s)/2):len(s)])
	else:
		print(s)
