import sys, fileinput

source = fileinput.input()

(n, m) = [int(l) for l in source.readline().strip().split()]

down = [[int(l) for l in source.readline().strip().split()] for nn in range(n)]
source.readline()

right = [[int(l) for l in source.readline().strip().split()] for mm in range(n+1)]
source.readline()

across = [[int(l) for l in source.readline().strip().split()] for nn in range(n)]

source.close()

print down
print right
print across

nums = [[ None for mm in range(m+1)] for nn in range(n+1)] 

print nums

nums[0][0] = 0

for i in range(1,n+1):
	print i
	nums[i][0] = nums[i-1][0] + down[i-1][0]

for j in range(1, m+1):
	nums[0][j] = nums[0][j-1] + right[0][j-1]

for i in range(1, n+1):
	for j in range(1, m+1):
		nums[i][j] = max(nums[i-1][j] + down[i-1][j], nums[i][j-1] + right[i][j-1], nums[i-1][j-1]+across[i-1][j-1])

print nums

print nums[n][m]