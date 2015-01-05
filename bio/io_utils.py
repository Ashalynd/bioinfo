import sys, fileinput

def read_input():
  source = fileinput.input()
  result = []
  for line in source:
    if line.startswith('Input'):
      continue
    if line.startswith('Output'):
      break
    result.append(line.strip())
  source.close()

  return result

def emit_array(data):
  print(" ".join(data))