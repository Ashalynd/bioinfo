import sys, fileinput

output = []

def read_input():
  source = fileinput.input()
  result = []
  active = result
  for line in source:
    if line.startswith('Input'):
      continue
    if line.startswith('Output'):
      active = output
      continue
    active.append(line.strip())
  source.close()

  return result

def read_adjacency_list(source, as_int = True):
  result = {}
  for line in source:
    key, values = [part.strip() for part in line.split('->')]
    values = values.split(',')
    if as_int: 
      values = [int(v) for v in values]
      key = int(key)
    result[key] = values
  return result

def generate_input(source, status):
  for line in source:
    if line.startswith('Input'):
      continue
    if line.startswith('Output'):
      status['output'] = True
      break
    yield line.strip()

def generate_output(source):
  for line in source:
    yield line.strip()

def generate_sorted(source):
  for output in sorted(list(source)):
    yield output

# method should return a generator
def generate_input_output(method, sort_output = False, compare = True):
  source = fileinput.input()
  status = {}
  result = method(generate_input(source, status))
  if 'output' in status and status['output'] and compare:
    output = generate_output(source)
    if sort_output:
      result = generate_sorted(result)
      output = generate_sorted(output)
    out = True
    for r in result:
      try:
        o = output.next()
        print r
        print o
        out = (o == r)
        if not out: break
      except StopIteration:
        out = False
        break
    source.close()
    print out
  else:
    source.close()
    for r in result:
      print r

def has_output():
  return not not output

def compare_with_output(result):
  local_result = result
  len_output = len(output)
  if len_output==1:
    if type(local_result) in (list, tuple):
      local_result = [" ".join([str(i) for i in result])]
    else:
      local_result = [str(result)]
  else:
    for line in local_result: line = " ".join([str(i) for i in line])
  return local_result==output

def stringify_array(data):
  return " ".join([str(i) for i in data])

def emit_array(data):
  print(stringify_array(data))

def gen_array(data):
  yield stringify_array(data)

def gen_lines(data, converter = None):
  for line in data:
    if not converter:
      yield line
    else:
      yield converter(line)

def gen(data): yield data

def emit_gen(data):
  for r in data:
    print r

def emit(data):
  if type(data) in (list, tuple):
    emit_array(data)
  else:
    print str(data)

def emit_or_compare(data):
  if has_output():
      print compare_with_output(data)
  else:
      emit(data)