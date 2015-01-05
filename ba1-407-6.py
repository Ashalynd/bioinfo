import bio.io_utils
import bio.pattern


def approximate_pattern_count(text, pattern, d):
  print "d: %s" % d
  count = 0
  pattern_len = len(pattern)
  limit = len(text)-pattern_len
  for i in xrange(limit+1):
    hd = bio.pattern.hamming(text[i:(i+pattern_len)], pattern)
    print i, text[i:i+pattern_len], pattern, hd, d, count
    if hd<=d:
      print "hd: %s, d: %s, hd<=d: %s" % (hd, d, hd<=d)
      count = count+1
  return count

text, pattern, d = bio.io_utils.read_input()[:3]
print pattern, d
count = approximate_pattern_count(text, pattern, int(d))
print "count: %s" % count