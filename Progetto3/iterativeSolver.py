import numpy as np
import time
import sys

from abc import abstractmethod
from scipy.sparse import identity, tril, csr_matrix
from scipy.sparse.linalg import spsolve_triangular

class GeneralIterativeSolver:

    def __init__(self, A, b):
        self.A = A
        self.b = b
        self.__norm_b = np.linalg.norm(b)
        self.__error = None
        self.__iterations = None
        self.__exec_time = None
        self.__result = None

    def __timing(f):
    	def wrap(*args):
        	time1 = time.perf_counter()
        	result = f(*args)
        	time2 = time.perf_counter()

	       	args[0].__exec_time = (time2-time1)
        	return result
    	return wrap

    def __relative_error(self):
        if self.__result is not None:
            real_sol = np.ones(self.A.shape[0])
            return np.linalg.norm(real_sol - self.__result) / np.linalg.norm(real_sol)

    @__timing
    def solve(self, tol, max_iterations=20000):
        
        current_x = np.zeros(self.b.size)
        k = 0
        current_error = 1

        while current_error > tol:
            residue = self.b - self.A.dot(current_x) 
            current_error = np.linalg.norm(residue) / self.__norm_b
            k += 1
            current_x = self.update(current_x, residue)
            if k >= max_iterations:
                sys.stdout.write("No solution found, number of max iterations passed")
                break

        self.__result = current_x
        self.__error = current_error
        self.__iterations = k
            

        return self.__result

    @abstractmethod
    def update(self, current_x, residue):
        pass

    @abstractmethod   
    def print_info(self):
    	if self.__iterations is not None and self.__exec_time is not None:
            sys.stdout.write("iterazioni = {:s} \nerrore_relativo = {:s} \ntempo_di_esecuzione = {:.3f} s\n".format(
                str(self.__iterations), 
                str(self.__relative_error()), 
                self.__exec_time))
            sys.stdout.flush()

class JacobiIterativeSolver(GeneralIterativeSolver):
    def __init__(self, A, b):
        super().__init__(A, b)
        self.__inverse_P = csr_matrix(identity(self.A.shape[0]) / self.A.diagonal())

    def update(self, current_x, residue):
        return current_x + self.__inverse_P.dot(residue)

    def print_info(self):
        sys.stdout.write("\nJacobi solution:\n")
        super().print_info()

class GaussSeidelIterativeSolver(GeneralIterativeSolver):

    def __init__(self, A, b):
        super().__init__(A, b)
        #self.__triangular_P = tril(A).todense()
        self.__triangular_P = tril(A).tocsr()

    def update(self, current_x, residue):
        #return current_x + self.__forward_substitution(self.__triangular_P, residue)
        return current_x + spsolve_triangular(self.__triangular_P, residue)

    def __forward_substitution(self, l, b):
        diag_elements = np.diag(l)
        n = l.shape[0]
        x = np.zeros(np.size(b))

        if diag_elements[0] == 0: 
            print("Error in forward substitution")
            return

        x[0] = b[0] / diag_elements[0]

        for i in range(1, n):
            if diag_elements[i] == 0:
                print("Error in forward_substitution")
                return
            x[i] = (b[i] - l[i, :].dot(x)) / diag_elements[i]

        return x

    def print_info(self):
        sys.stdout.write("\nGauss-Seidel solution:\n")
        super().print_info()

class GradientIterativeSolver(GeneralIterativeSolver):

    def __init__(self, A, b):
        super().__init__(A, b)

    def update(self, current_x, residue):
        top = residue.dot(residue)
        bot = residue.dot(self.A.dot(residue))
        alpha = top / bot
        return current_x + alpha * residue

    def print_info(self):
        sys.stdout.write("\nGradient method solution:\n")
        super().print_info()

class ConjugateGradientIterativeSolver(GeneralIterativeSolver):

    def __init__(self, A, b):
        super().__init__(A, b)
        self.__direction = None

    def update(self, current_x, residue):
        if self.__direction is None:
            self.__direction = residue
        else:
            beta = self.__direction.dot(self.A.dot(residue)) / self.__direction.dot(self.A.dot(self.__direction))
            self.__direction = residue - beta * self.__direction
        alpha = self.__direction.dot(residue) / self.__direction.dot(self.A.dot(self.__direction))
        return current_x + alpha * self.__direction

    def print_info(self):
        sys.stdout.write("\nConjugate Gradient method solution:\n")
        super().print_info()