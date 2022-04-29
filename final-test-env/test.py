x = "1 2 3 4"
x = x.split()
x = map(lambda a : int(a), x)
print(sum(x))
