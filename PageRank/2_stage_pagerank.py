import numpy as np
L = np.array([[0,1/2,1/3,0,0,0],
             [1/3,0,0,0,1/2,0],
             [1/3, 1/2,0,1,0,1/2],
             [1/3,0,1/3,0,1/2,1/2],
             [0,0,0,0,0,0],
             [0,0,1/3,0,0,0]])

r_prev = 100 * np.ones(6) / 6
r_next = L @ r_prev

for num in r_next:
    print(round(num, 3))

for i in range(10):
    r_prev = r_next
    r_next = L @ r_prev

for num in r_next:
    print(round(num, 3))

while np.linalg.norm(r_prev - r_next) >= 0.01:
    r_prev = r_next
    r_next = L @ r_prev

for num in r_next:
    print(round(num, 3))
