letters = ['A','C','G','T'] #DNA alphabet
letters_map = dict([(letter, index) for (index, letter) in enumerate(letters)])
letters_num = len(letters)

# counts how many times pattern appears in the text (including overlaps)
def pattern_count(text, pattern):
  count = 0
  len_text = len(text)
  len_pattern = len(pattern)
  limit = len_text-len_pattern
  for i in xrange(limit+1):
    if text[i:(i+len_pattern)] == pattern:
      count +=1
  return count

def pattern_to_number(pattern):
  number = 0
  for letter in pattern:
    number*=letters_num
    number+=letters_map[letter]
  return number

def number_to_pattern(number, k):
  pattern = ''
  remainder = number
  index = 0
  while(index<k):
    letter_index = remainder % letters_num
    letter = letters[letter_index]
    pattern = letter + pattern
    if remainder <=0:
      break
    remainder = (remainder - letter_index) / letters_num
    index +=1
  return pattern

def reverse(pattern):
  result = ''
  for letter in pattern[::-1]:
    result += letters[letters_num-letters_map[letter]-1]
  return result

def hamming(pattern1, pattern2):
  result = 0
  pattern_len = len(pattern1)
  if len(pattern2)!=pattern_len:
    return -1
  for i in xrange(pattern_len):
    if pattern1[i]!=pattern2[i]:
      result+=1
  return result

# skew = G - C
def min_skew(pattern):
  cur_diff = 0
  pattern_len = len(pattern)
  total_diff, total_index = pattern_len, 0
  for i in xrange(pattern_len):
    if cur_diff < total_diff:
      total_index = i
      total_diff = cur_diff
    if pattern[i]=='C':
      cur_diff -=1
    if pattern[i]=='G':
      cur_diff +=1
    print(i, cur_diff, pattern[i])
  return total_index