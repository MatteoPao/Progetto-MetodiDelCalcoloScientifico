import numpy as np

from dct2 import dct2, idct2

'''
COMPRESS_MATRIX
Input: matrice, intero f, intero d
Questa funzione divide in blocchi la matrice, li comprime e infine li riposizona nel punto di partenza 
'''
def compress_matrix(mat, f, d):
    #Scarto gli avanzi della matrice
    mat = remove_margin(mat, f)
    row_block = int(mat.shape[0] / f)
    col_block = int(mat.shape[1] / f)

	#Comprimo la matrice in blocchi di dimensione f
    for x in range(0,row_block):
    	for y in range(0,col_block):
    		st_x = x * f
    		st_y = y * f
    		block = mat[st_x : st_x+f, st_y : st_y+f].copy()
    		mat[st_x : st_x+f, st_y : st_y+f] = compress_block(block, d)
    return mat

'''
REMOVE_MARGIN
Input: matrice, intero f
Questa funzione rimuove i margine basso e destro della matrice che non è divisibile per f
'''
def remove_margin(mat, f):
	y_margin = mat.shape[0] - (mat.shape[0] % f)
	x_margin = mat.shape[1] - (mat.shape[1] % f)
	return mat[:y_margin, :x_margin]

'''
COMPRESS_BLOCK
Input: matrice, intero d
Questa funzione comprime i singoli blocchi, taglia i valori secondo d ed inverte la compressione
'''
def compress_block(block, d):
    #Applico la DCT2 al Blocco
    block, t = dct2(block, False)
    
    #Elimino le fequenze che superano la solgia di taglio d
    for x in range(0, block.shape[0]):
    	for y in range(0, block.shape[1]):
    		if(x + y >= d):
    			block[x][y] = 0

	#Applico la DCT2 inversa al blocco
    block = idct2(block)
	#Arrotondo i valori ad intero
    block = np.rint(block)
    block = block.astype(int)
	#Arrotondo i valori che non rispettano i margini (0, 255)
    block = np.where(block > 255, 255, block)
    block = np.where(block < 0, 0, block)
    return block