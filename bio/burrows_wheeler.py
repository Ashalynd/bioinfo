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
    empty_result = 0 if not suffix_array else []
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
    lastfirst = [0]*len(pos)
    for index, letter in enumerate(first):
        lastpos = letters[letter][pos[index]]
        lastfirst[lastpos] = index
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
                return empty_result
            if bottom_index+top_index>=0:
                top_index+=top
                bottom_index +=top
#                print "top_index", top_index, "bottom_index", bottom_index, "symbol", symbol
                top = lastfirst[top_index]
                bottom = lastfirst[bottom_index]
            else:
                return empty_result
        else:
            if not suffix_array:
                return bottom-top+1
            else:
                return [suffix_array[i] for i in xrange(top, bottom+1)]

def count(text, with_bwt_transform = False):
    if with_bwt_transform: text = bwt(text)
    sorted_letters = sorted(list(set(text)))
    letters = {letter:index for (index, letter) in enumerate(sorted_letters)}
    outcome = []
    row = [0]*len(letters)
    for letter in text:
        outcome.append(row)
        index = letters[letter]
        row = row[:index]+[row[index]+1]+row[index+1:]
    outcome.append(row) # add the last row
    return outcome, letters

def better_bwmatching(last, pattern, counts = None, letter_places = None):
    result = 0
    first = sorted(last)
    first_occurence = {}
    prev_letter = ''
    for index, letter in enumerate(first):
        if letter == prev_letter: continue
        first_occurence[letter] = index
        prev_letter = letter
#    print "first_occurence", first_occurence
    if not counts or not letter_places: counts, letter_places = count(last)
#    print "counts", counts, "letter_places", letter_places
    top = 0
    bottom = len(last)-1
    pattern_index = len(pattern)-1
    while top <= bottom:
#        print "index", pattern_index, "top", top, "bottom", bottom, "fragment", last[top:bottom]
        if pattern_index < 0: 
            result = bottom - top + 1
            break
        symbol = pattern[pattern_index]
        pattern_index-=1
#        print "symbol", symbol
        if not symbol in last[top:bottom+1]: break
        top = first_occurence[symbol] + counts[top][letter_places[symbol]]
        bottom = first_occurence[symbol] + counts[bottom+1][letter_places[symbol]]-1
    return result
