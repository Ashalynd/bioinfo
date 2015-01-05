import sys

nums = []

def num_paths(x, y, w, h):
	global nums
	if nums[y][x] is None:
		if (x == w) and ( y == h):
			nums[y][x] = 1
		elif (x == w) and (y < h):
			nums[y][x] = num_paths(x, y+1, w, h)
		elif (x < w) and (y == h):
			nums[y][x] = num_paths(x+1, y, w, h)
		else:
			nums[y][x] = num_paths(x+1, y, w, h) + num_paths(x, y+1, w, h)
	return nums[y][x]

(h, w) = [int(l) for l in sys.argv[1:]]

print h,w
nums = [[ None for n in range(w+1)] for m in range(h+1)] 

res = num_paths(0,0, w, h)

print nums

print res 
