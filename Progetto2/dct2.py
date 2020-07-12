import sys
import numpy as np
import math as m
import time

from scipy.fftpack import dct, idct

def timing(f):
    def wrap(*args):
        time1 = time.perf_counter()
        ret = f(args[0])
        time2 = time.perf_counter()
        final_time = (time2-time1)
        if args[1]:
        	sys.stdout.write('{:s} function took {:.6f} s'.format(f.__name__, final_time) + "\n")
        	sys.stdout.flush()
        return ret, final_time
    return wrap

def my_dct(mat):
	result_mat = np.zeros(mat.shape)
	_sum = 0
	n = mat.shape[0]

	for j in range(0, n):
		for k in range(0, n):
			alpha = m.sqrt(2/n) if k != 0 else (1/m.sqrt(n))
			for i in range(0, n):
				_sum += m.cos((m.pi * k * (2*i + 1))/(2*n)) * mat[j][i]	

			result_mat[j][k] = alpha * _sum
			_sum = 0
	return result_mat

@timing
def my_dct2(mat):
	return my_dct(my_dct(mat.T).T)

@timing
def dct2(mat):
	return dct(dct(mat.T, norm='ortho').T, norm='ortho')

def idct2(mat):
    return idct(idct(mat.T, norm='ortho').T, norm='ortho')

