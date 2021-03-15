import numpy as np

n, d = input().split()
n, d = int(n), float(d)
L = np.zeros((n,n))
for i in range(n):
    line = [float(j) for j in input().split()]
    L[i] = line

M = d*L + np.ones((n,n)) * (1-d)/n
r_prev = 100 * np.ones(n) / n
r_next = M @ r_prev

while np.linalg.norm(r_prev - r_next) >= 0.01:
    r_prev = r_next
    r_next = M @ r_prev

for num in r_next:
    print(round(num, 3))
