"""
Imagine a hypothetical world in which there are two amino acids, X and Z, having respective masses 2 and 3. 
How many linear peptides can be formed from these amino acids having mass equal to 24? 
(Remember that the order of amino acids matters.)
"""
import bio.io_utils

mass, coins = bio.io_utils.read_input()
mass = int(mass)
coins = [int(c) for c in coins.split(',')]

print mass, coins

def calc_combinations(mass, coins):
    print "mass", mass, "coins", coins
    if mass==0:
        return 1
    useful_coins = [coin for coin in coins if coin<=mass]
    if len(useful_coins)==0:
        print "mass", mass, "coins", coins, "0"
        return 0
    if len(useful_coins)==1:
        result = 1 if useful_coins[0]==mass else 0
        print "mass", mass, "coins", coins, result
        return result
    result = sum([calc_combinations(mass-i, coins) for i in coins])
    print "mass", mass, "coins", coins, result
    return result

result = calc_combinations(mass, coins)
print result