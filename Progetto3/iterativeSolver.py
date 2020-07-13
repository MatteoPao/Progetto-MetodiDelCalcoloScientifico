import numpy as np
import time
import sys

from abc import abstractmethod
from scipy.sparse import identity, tril, csr_matrix
from scipy.sparse.linalg import spsolve_triangular

'''
GENERAL ITERATIVE SOLVER
Superclasse dei quattro metodi  iterativi
'''
class GeneralIterativeSolver:

	#Costruttore, richiede la matrice A dei coefficenti e il vettore b dei termini noti
    def __init__(self, A, b):
        self.A = A
        self.b = b
        self.__norm_b = np.linalg.norm(b)
        self.__error = None
        self.__iterations = None
        self.__exec_time = None
        self.__result = None

    '''
	TIMING
	Metodo privato - Calcola i tempi di esecuzione della funzione decorata con esso
	''' 
    def __timing(f):
    	def wrap(*args):
        	time1 = time.perf_counter()
        	result = f(*args)
        	time2 = time.perf_counter()

	       	args[0].__exec_time = (time2-time1)
        	return result
    	return wrap

    '''
	RELATIVE_ERROR
	Metodo privato - Calcola la distanza tra la soluzione trovata e la soluzione esatta
	''' 
    def __relative_error(self):
        if self.__result is not None:
            real_sol = np.ones(self.A.shape[0])
            return np.linalg.norm(real_sol - self.__result) / np.linalg.norm(real_sol)

    '''
	SOLVE
	Metodo pubblico - Implementa il generico algoritmo per un risolutore iterativo
	''' 
    @__timing
    def solve(self, tol, max_iterations=20000):
        
        current_x = np.zeros(self.b.size)
        k = 0
        current_error = 1

        while current_error > tol:
        	#Calcolo del residuo e del residuo scalato
            residue = self.b - self.A.dot(current_x) 
            current_error = np.linalg.norm(residue) / self.__norm_b
            k += 1

            #Calcolo del passo successivo X_k+1 da X_k
            current_x = self.update(current_x, residue)

            #Se supero le iterazioni massime disponibili interrompo
            if k >= max_iterations:
                sys.stdout.write("No solution found, number of max iterations passed")
                break

        self.__result = current_x
        self.__error = current_error
        self.__iterations = k
            

        return self.__result

    '''
	UPDATE
	Metodo astratto - viene implementato dalle sottoclassi
	''' 
    @abstractmethod
    def update(self, current_x, residue):
        pass

    '''
	PRINT_INFO
	Metodo astratto - stampa i risultati a seconda del tipo di metodo iterativo utilizzato
	''' 
    @abstractmethod   
    def print_info(self):
    	if self.__iterations is not None and self.__exec_time is not None:
            sys.stdout.write("iterazioni = {:s} \nerrore_relativo = {:s} \ntempo_di_esecuzione = {:.3f} s\n".format(
                str(self.__iterations), 
                str(self.__relative_error()), 
                self.__exec_time))
            sys.stdout.flush()


'''
METODO DI JACOBII
Primo metodo iterativo stazionario
'''
class JacobiIterativeSolver(GeneralIterativeSolver):
	#Costruttore
    def __init__(self, A, b):
        super().__init__(A, b)
        self.__inverse_P = csr_matrix(identity(self.A.shape[0]) / self.A.diagonal())

    #UPDATE
    def update(self, current_x, residue):
        return current_x + self.__inverse_P.dot(residue)

    def print_info(self):
        sys.stdout.write("\nJacobi solution:\n")
        super().print_info()


'''
METODO DI GAUSS-SIDEL
Secondo metodo iterativo stazionario
'''
class GaussSeidelIterativeSolver(GeneralIterativeSolver):
	
	#Costruttore	
    def __init__(self, A, b):
        super().__init__(A, b)
        #self.__triangular_P = tril(A).todense()
        self.__triangular_P = tril(A).tocsr()

    #UPDATE (è stato utilizzato il metodo spsolve della libreria scipy, poichè funziona con matrici csr)
    def update(self, current_x, residue):
        #return current_x + self.__forward_substitution(self.__triangular_P, residue)
        return current_x + spsolve_triangular(self.__triangular_P, residue)

    # Questo metodo non è stato utilizzato nel calcolo finale dei tempi(troppo lento, richiede matrice densa)
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


'''
METODO DEL GRADIENTE
Primo metodo iterativo non stazionario
'''
class GradientIterativeSolver(GeneralIterativeSolver):
	#Costruttore
    def __init__(self, A, b):
        super().__init__(A, b)

    #UPDATE
    def update(self, current_x, residue):
        top = residue.dot(residue)
        bot = residue.dot(self.A.dot(residue))
        alpha = top / bot
        return current_x + alpha * residue

    def print_info(self):
        sys.stdout.write("\nGradient method solution:\n")
        super().print_info()


'''
METODO DEL GRADIENTE CONIUGATO
Secondo metodo iterativo non stazionario
'''
class ConjugateGradientIterativeSolver(GeneralIterativeSolver):
	#Costruttore
    def __init__(self, A, b):
        super().__init__(A, b)
        self.__direction = None

    #UPDATE
    def update(self, current_x, residue):
    	#Se è la prima iterazione direction è uguale al residuo, altrimenti calcolo la direzione k+1 e la utilizzo subito
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