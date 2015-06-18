import sys, fileinput

output = []

def eat_line(source):
    source.next()

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
    if key not in result:
      result[key] = values
    else:
      result[key].extend(values)
  return result

def read_adjacency_list_with_weight(source, as_int = True):
  result = {}
  for line in source:
    parent, payload = [part.strip() for part in line.split('->')]
    child, weight = payload.split(':')
    if as_int:
      parent = int(parent)
      child = int(child)
      weight = int(weight)
    if not parent in result:
      result[parent] = {}
    if not child in result[parent]:
      result[parent][child] = weight
  return result

def read_float_list(source):
    result = []
    for line in source:
        row = tuple([float(elem) for elem in line.split()])
        result.append(row)
    return result

def read_int_matrix(source):
    result = []
    for line in source:
        row = [int(elem) for elem in line.split()]
        result.append(row)
    return result

def read_elements(source):
    return [p for p in source.next().split()]

def read_state_matrix(source):
    separator = '-'
    row_states = read_elements(source)
    probs = {}
    for line in source:
        if line[0] == separator: break
        elements = line.split()
        state, state_probs = elements[0], [float(p) for p in elements[1:]]
        probs[state] = {state:prob for (state, prob) in zip(row_states, state_probs)}
    return probs

def generate_input(source, status):
  for line in source:
    if not line.strip(): 
      continue
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
        out = (o.strip() == r.strip())
        if not out: break
      except StopIteration:
        out = False
        break
    source.close()
    print out
  else:
    source.close()
    if sort_output:
      result = generate_sorted(result)
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
  return local_result.strip()==output.strip()

def prob_format(x):
  return '0' if not x else ('1.0' if x==1 else ('%.3f' % x).rstrip('0'))

def stringify_array_format(data, concat = ' ', format = '%s'):
  if type(format) == str:
    return concat.join([format % i for i in data])
  else: # assume 'function'
    return concat.join([format(i) for i in data])

def stringify_array(data, concat = ' '):
  return concat.join([str(i) for i in data])

def emit_array(data, concat = ' '):
  print(stringify_array(data, concat))

def gen_array(data, concat = ' '):
  yield stringify_array(data, concat)

def gen_matrix(data, concat = ' '):
  for row in matrix:
    return gen_array(row)

def gen_matrices(states, external_states, transition_probs, emission_probs, delim = '\t', format = '%.3f'):
    yield delim+ stringify_array(states, delim)
    for i, s in enumerate(states):
        yield s+delim+ stringify_array_format(transition_probs[i], concat=delim, format=format)
    yield('--------')
    yield delim + stringify_array(external_states, delim)
    for i, s in enumerate(states):
        yield s+ delim + stringify_array_format(emission_probs[i], concat=delim, format=format)


def gen_lines(data, converter = None):
  for line in data:
    if not converter:
      yield line
    else:
      yield converter(line)

def gen_lines_format(data, concat = ' ', format = '%s'):
  for line in data:
    yield stringify_array_format(line, concat, format)


def gen(data): yield str(data)

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