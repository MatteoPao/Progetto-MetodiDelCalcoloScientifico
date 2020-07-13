import sys
import numpy as np
import math as m
import time

from scipy.fftpack import dct, idct

'''
TIMING
Questa funzione viene chiamata wrapper.
Le funzioni che hanno nella loro intestazione il decoratore @timing  attivano questa funzione quando vengono chiamate
'''
def timing(f):
    def wrap(*args):
    	#viene salvato il tempo all'inizio della funzione
        time1 = time.perf_counter()

        #viene eseguita la funzione chiamante
        ret = f(args[0])

        #viene salvato il tempo alla fine della funzione
        time2 = time.perf_counter()
        final_time = (time2-time1)

        #se segnalato in input, viene stampato il log
        if args[1]:
        	sys.stdout.write('{:s} function took {:.6f} s'.format(f.__name__, final_time) + "\n")
        	sys.stdout.flush()
        return ret, final_time
    return wrap

'''
MY_DCT
Input: una matrice
Questa funzione implementa l'algoritmo di DCT e lo applica su ogni riga della matrice in ingresso
'''
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

'''
MY_DCT2
Input: una matrice
Viene calcolata la DCT2 con due chiamate a MY_DCT e due trasposizioni di matrice
'''
@timing
def my_dct2(mat):
	return my_dct(my_dct(mat.T).T)

'''
DCT2
Input: una matrice
Viene calcolata la DCT2 con due chiamate a scipy.DCT e due trasposizioni di matrice
'''
@timing
def dct2(mat):
	return dct(dct(mat.T, norm='ortho').T, norm='ortho')

'''
IDCT2
Input: una matrice
Viene calcolata la IDCT2 con due chiamate a scipy.IDCT e due trasposizioni di matrice
'''
def idct2(mat):
    return idct(idct(mat.T, norm='ortho').T, norm='ortho')

