import numpy as np
import matplotlib.pyplot as plt
import iterativeSolver as lss
import sys

from scipy.sparse import coo_matrix
from scipy.io import mmread

TOL = [1e-4, 1e-6, 1e-8, 1e-10]

def main():

	filename = "Matrici_Progetto3/vem1.mtx"

	mat_A = read_sparse_mtx(filename)
	print(np.count_nonzero(mat_A.toarray()))
	print(mat_A.shape[0])

	tmp = np.ones(mat_A.shape[0])
	b = mat_A.dot(tmp)
	plt.spy(mat_A, precision = 0.001, markersize = 0.3)
	plt.show()

	jacobiSolver = lss.JacobiIterativeSolver(mat_A, b)
	gaussSeidelSolver = lss.GaussSeidelIterativeSolver(mat_A, b)
	gradientSolver = lss.GradientIterativeSolver(mat_A, b)
	conjugateGradientSolver = lss.ConjugateGradientIterativeSolver(mat_A, b)

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


def read_sparse_mtx(filename):
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
	print("File imported: " ,filename)
	print()
	return coo.tocsr()

if __name__ == "__main__":
	main()