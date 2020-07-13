import numpy as np
import os
import sys
import argparse
import matplotlib.pyplot as plt

from scipy.io import mmread, mmwrite
from dct2 import my_dct2, dct2

#Il parser è l'oggetto che gestisce i valori dati in ingresso da console quando si chiama questa procedura.
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--num_rep', type=int, default=5, help='Number of different matrix to operate for')
parser.add_argument('-s', '--size_mat', type=int, default=10, help='Increase in size between one matrix and another')
parser.add_argument('--log', default = False, action = 'store_true', help='Boolean value to view the console log')
args = parser.parse_args()

'''
PLOT_GRAPH
Input: tre vettori, 
size - contiene i valori di dimensione delle matrici
my_time - contiene i tempi di esecuzione della mia funzione dct2
lib_time - contiene i tempi di esecuzione della funzione dct2 di scipy

Questa funzione disegna graficamente i tempi in un grafico semilogaritmico
'''
def plot_graph(size, my_time, lib_time):
	plt.grid(True, which='both')
	plt.xlabel('Size')
	plt.ylabel('Seconds')
	plt.xticks(size)
	line1, = plt.semilogy(size, my_time)
	line2, = plt.semilogy(size, lib_time)
	plt.legend([line1, line2], ["my_dct2", "dct2"])
	plt.show()

'''
RANDOM_MATRIX
Input: intero quantity, intero size
Questa funzione genera "quantity" matrici, di "size" dimensione e le salva nella cartella TestMatrix in formato .mtx
'''
def randomMatrix(quantity, size):
	
	for x in range(0, quantity):
		sizeMat = size * (x+1)
		namefile = ".\\TestMatrix\\testMat_" + str(sizeMat) + "x" + str(sizeMat)

		A = np.random.randint(256, size=(sizeMat,sizeMat))
		mmwrite(namefile, A)

'''
MAIN
Il main effettua dei test delle due DCT2 su delle matrici randomiche e riporta i risultati su un grafico
'''
def main():

	num_repetition = args.num_rep
	size_multiplicator = args.size_mat

	my_time = np.zeros(num_repetition)
	lib_time = np.zeros(num_repetition)
	size = np.zeros(num_repetition, dtype = np.int32)

	for x in range(0, num_repetition):
		#Cerco la matrice della giusta dimensione
		size[x] = size_multiplicator * (x+1)
		filename = "TestMatrix/testMat_" + str(size[x]) + "x" + str(size[x]) + ".mtx"
		
		#Se la matrice filename non esiste ne genero una e la apro
		if not os.path.isfile(filename):
			randomMatrix(num_repetition, size_multiplicator)
		A = mmread(filename)

		if args.log:
			print("\nDCT2 on: testMat_" + str(size[x]) + "x" + str(size[x]))

		#Calcolo la dct2 di scipy e la dct2 artigianale
		resmat, lib_time[x] = dct2(A, args.log)
		my_resmat, my_time[x] = my_dct2(A, args.log)

	#infine stampo i risultati su un grafo
	plot_graph(size, my_time, lib_time)

if __name__ == "__main__":
    main()