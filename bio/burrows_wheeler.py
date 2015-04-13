def bwt(s):
    l = len(s)
    ll = [s]
    for i in xrange(1,l):
        next_s = ll[i-1][1:]+ll[i-1][0]
        ll.append(next_s)
    print("ll", ll)
    ll.sort()
    print("ll", ll)
    return ''.join([l[-1] for l in ll])

def reverse_bwt(last):
    first = sorted(last)
    print("first", first)
    pos = []
    prev_letter = ''
    cur_pos = 0
    for letter in first:
        if prev_letter==letter:
            cur_pos+=1
        else:
            cur_pos = 0
        pos.append(cur_pos)
        prev_letter = letter
    print "pos", pos
    letters = dict([(l, []) for l in set(last)])
    for index, letter in enumerate(last):
        letters[letter].append(index)
    print "letters", letters
    prev_pos = last.find('$')
    result = ""
    for i in xrange(len(last)):
        next_letter = first[prev_pos]
        result += next_letter
        prev_pos = letters[next_letter][pos[prev_pos]]
        print next_letter, prev_pos
    return result