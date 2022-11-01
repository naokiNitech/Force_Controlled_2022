import numpy as np

l1 = np.linspace(0, 10, 200)
l2 = np.linspace(0, 10, 200)
iter1 = iter(l1)
iter2 = iter(l2)

print(l1)
print(len(l1))

flag = 0

for _ in range(len(l1)):
    if flag == 0:
        print(next(iter1))
        flag = 1
    elif flag == 1:
        print(next(iter1))
        print(next(iter2))