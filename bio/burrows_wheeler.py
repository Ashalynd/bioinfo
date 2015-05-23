def bwt(s, with_suffix_array = False):
    l = len(s)
    ll = [s]
    for i in xrange(1,l):
        next_s = ll[i-1][1:]+ll[i-1][0]
        ll.append(next_s)
#    print("ll", ll)
    ll.sort()
#    print("ll", ll)
    if not with_suffix_array:
        return ''.join([elem[-1] for elem in ll])
    else:
        return ''.join([elem[-1] for elem in ll]), [l-elem.find('$')-1 for elem in ll]

def reverse_bwt(last):
    first = sorted(last)
#    print("first", first)
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
#    print "pos", pos
    letters = dict([(l, []) for l in set(last)])
    for index, letter in enumerate(last):
        letters[letter].append(index)
#    print "letters", letters
    prev_pos = last.find('$')
    result = ""
    for i in xrange(len(last)):
        next_letter = first[prev_pos]
        result += next_letter
        prev_pos = letters[next_letter][pos[prev_pos]]
#        print next_letter, prev_pos
    return result

def bwmatching(last, pattern, suffix_array = None):
#    print "last", last, "pattern", pattern
#    if suffix_array: print "suffix_array", suffix_array
    first = sorted(last)
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
    letters = dict([(l, []) for l in set(last)])
    for index, letter in enumerate(last):
        letters[letter].append(index)
#    print "letters", letters
#    print "pos", pos
    lastfirst = [0]*len(pos)
#    print lastfirst
    for index, letter in enumerate(first):
        lastpos = letters[letter][pos[index]]
        lastfirst[lastpos] = index
#    print "lastfirst", lastfirst, "len", len(lastfirst)
    top = 0
    bottom = len(last)-1
    while top<=bottom:
#        print "top", top, "bottom", bottom
        if len(pattern):
            symbol = pattern[-1]
            pattern = pattern[:-1]
            sub_last = last[top:bottom+1]
            top_index = sub_last.find(symbol)
            if top_index>=0: 
                bottom_index = sub_last.rfind(symbol)
            else:
                if not suffix_array:
                    return 0
                else:
                    return []
            if bottom_index+top_index>=0:
                top_index+=top
                bottom_index +=top
#                print "top_index", top_index, "bottom_index", bottom_index, "symbol", symbol
                top = lastfirst[top_index]
                bottom = lastfirst[bottom_index]
            else:
                if not suffix_array:
                    return 0
                else:
                    return []
        else:
            if not suffix_array:
                return bottom-top+1
            else:
                return [suffix_array[i] for i in xrange(top, bottom+1)]
