import numpy as np
import matplotlib.pyplot as plt
import iterativeSolver as lss
import sys
import os

from scipy.sparse import coo_matrix
from scipy.io import mmread

TOL = [1e-4, 1e-6, 1e-8, 1e-10]

def main(argv):

	#Se viene data un file in input apro quello, altrimenti spa1 viene utilizzato di default
	if len(argv):
		filename = "Matrici_Progetto3/"+ argv[0]+".mtx"
	else:
		filename = "Matrici_Progetto3/spa1.mtx"

	#Chiamo la funzione di appoggio read_sparse_matrix
	mat_A = read_sparse_mtx(filename)

	#Creo i termini noti b utilizzando il vettore tmp (x)
	tmp = np.ones(mat_A.shape[0])
	b = mat_A.dot(tmp)
	
	#Creo gli oggetti dei quattro tipi di iterative solver
	jacobiSolver = lss.JacobiIterativeSolver(mat_A, b)
	gaussSeidelSolver = lss.GaussSeidelIterativeSolver(mat_A, b)
	gradientSolver = lss.GradientIterativeSolver(mat_A, b)
	conjugateGradientSolver = lss.ConjugateGradientIterativeSolver(mat_A, b)

	#Per ogni tolleranza risolvo il sistema con ognuno dei quattro metodi e stampo i risultati
	for tol in TOL:

		sys.stdout.write("\nTolleranza = "+ str(tol))
		sys.stdout.write("\n-------------------------")
		jacobiSolver.solve(tol)
		jacobiSolver.print_info()

		gaussSeidelSolver.solve(tol)
		gaussSeidelSolver.print_info()

		gradientSolver.solve(tol)
		gradientSolver.print_info()

		conjugateGradientSolver.solve(tol)
		conjugateGradientSolver.print_info()
		sys.stdout.write("-------------------------\n")
		sys.stdout.flush()


'''
READ_SPARSE_MATRIX
Questa funzione legge i file .mtx scritti nel formato dato dal progetto
(la funzione mmread di scipy dava degli errori per colpa dell'intestazione)
'''
def read_sparse_mtx(filename):
	if not os.path.isfile(filename):
		print("[ERROR] Il file " + filename + " non esiste")
		sys.exit()

	file = open(filename, "r")
	dim = file.readline().strip().split("  ")
	row = []
	col = []
	data =[]

	for line in file:
		entry = line.strip().split("  ")
		row.append(int(entry[0]) - 1)
		col.append(int(entry[1]) - 1)
		data.append(float(entry[2]))

	coo = coo_matrix((data, (row, col)), shape=(int(dim[0]), int(dim[1])))
	print("\nFile imported: " ,filename)
	return coo.tocsr()

if __name__ == "__main__":
	main(sys.argv[1:])