def merge(dr):
  if dr == 2:

    return dr
  else:

    return merge(dr/2) + dr
print(merge(16))
