import numpy as np
L = np.array([[0,1/2,1/3,0,0,0],
             [1/3,0,0,0,1/2,0],
             [1/3, 1/2,0,1,0,1/2],
             [1/3,0,1/3,0,1/2,1/2],
             [0,0,0,0,0,0],
             [0,0,1/3,0,0,0]])
from io import StringIO
s = StringIO()
np.savetxt(s, L, fmt="%.3f")
print(s.getvalue())
e_vals, e_vecs = np.linalg.eig(L)
vec = np.transpose(e_vecs)[0]
vec = vec * 100 / sum(vec)
for i in range(len(vec)):
    print(round(vec[i].real,3))
