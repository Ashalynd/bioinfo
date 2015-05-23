def is_cycle(array):
	arr_set = set()
	next = 0
	count = 0
	arr_len = len(array)
	while count<arr_len:
		next = array[next]
		if next > arr_len: return False
		if next in arr_set: return True
		arr_set.add(next)
		count +=1
	return False
