import numpy as np
from io import StringIO
L2 = np.array([[0,1/2,1/3,0,0,0,0],
             [1/3,0,0,0,1/2,0,0],
             [1/3, 1/2,0,1,0,1/3,0],
             [1/3,0,1/3,0,1/2,1/3,0],
             [0,0,0,0,0,0,0],
             [0,0,1/3,0,0,0,0],
              [0,0,0,0,0,1/3,1]])

'''1 problem'''
s = StringIO()
np.savetxt(s, L2, fmt="%.3f")
print(s.getvalue())

'''2 problem'''
r_prev = 100 * np.ones(7) / 7
r_next = L2 @ r_prev
while np.linalg.norm(r_prev - r_next) >= 0.01:
    r_prev = r_next
    r_next = L2 @ r_prev

for num in r_next:
    print(round(num, 3))
print()
'''3 problem'''
d = 0.5
J = np.ones(L2.shape)
M = d*L2 + J * (1-d)/L2.shape[0]

r_prev = 100 * np.ones(7) / 7
r_next = M @ r_prev
while np.linalg.norm(r_prev - r_next) >= 0.01:
    r_prev = r_next
    r_next = M @ r_prev

for num in r_next:
    print(round(num, 3))
