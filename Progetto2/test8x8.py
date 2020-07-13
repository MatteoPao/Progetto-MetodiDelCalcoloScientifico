import numpy as np

from scipy.io import mmread
from dct2 import my_dct2, dct2

'''
Questo breve test controlla 
il corretto funzionamento della dct2 implementata
'''
filename = "TestMatrix/testMat_8x8.mtx" 
A = mmread(filename)

my_resmat, my_time = my_dct2(A, False)

print(my_resmat)