def chunkList(self, n, array):
  avg = len(array) / float(n * n)
  result = []
  row = []
  last = 0.0

  while last < len(array):
    tmp = array[int(last):int(last + avg)]
    row.append(0 if not tmp else (sum(tmp)/len(tmp), 2))
    if len(row) == n and (last + avg) < len(array):
      result.append(row)
      row = []
    last += avg
  if len(result) == 19:
    result.append(row)

  return result