import bio.io_utils
import bio.pattern

pattern1, pattern2 = bio.io_utils.read_input()[:2]
print "pattern1: %s, pattern2: %s" % (pattern1, pattern2)
hd = bio.pattern.hamming(pattern1, pattern2)
print "hamming_distance: %s" % hd