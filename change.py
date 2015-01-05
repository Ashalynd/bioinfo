import sys, fileinput

source = fileinput.input()

money = int(source.readline().strip())
coins = [int(c) for c in source.readline().strip().split(',')]

mnc = [float('inf') for i in range(money+1)]
mnc[0] = 0

for m in range(money+1):
	for coin in coins:
		if m>=coin:
			if mnc[m-coin] +1 < mnc[m]:
				mnc[m] = mnc[m-coin]+1

print mnc[money]

