import numpy as np
n = int(input())
names = input().split()
L = np.zeros((n,n))
for i in range(n):
    line = [float(j) for j in input().split()]
    L[i] = line
query_name = input()
d = 0.5
M = d*L + np.ones((n,n)) * (1-d)/n
r_prev = 100 * np.ones(n) / n
r_next = M @ r_prev

while np.linalg.norm(r_prev - r_next) >= 0.01:
    r_prev = r_next
    r_next = M @ r_prev

websites = dict()
for i in range(n):
    websites[names[i]] = r_next[i]
k = 5
if query_name in websites:
    print(query_name)
    del websites[query_name]
    k -= 1
websites = sorted(websites.items(), key=lambda x: (x[1], x[0]), reverse=True)
for key in websites:
    print(key[0])
    k -= 1
    if k == 0:
        break

