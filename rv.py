num_linhas  = 4
num_colunas = 4

mapa = []

def coordenada_linha(coordenada):
	return coordenada[0]

def coordenada_coluna(coordenada):
	return coordenada[1]

def confirma_coordenada(argumento):
	if argumento == ():
		return False

	elif isinstance (argumento, tuple)\
				and len(argumento) == 2 \
				and isinstance(coordenada_linha(argumento),int) \
				and isinstance(coordenada_coluna(argumento),int)\
				and (0 <= coordenada_linha(argumento) < num_linhas) \
				and (0 <= coordenada_coluna(argumento) < num_colunas):
		return True
	raise ValueError ('A coordenada inserida não existe')


def coordenadas_iguais(coordenada1, coordenada2):
	return coordenada1 == coordenada2


def cria_mapa(num_linhas,num_colunas):
	mapa=[]
	for i in range(num_linhas):
		line = []
		for j in range(num_colunas):
			coordinate = (i, j)
			line.append(coordinate)
		mapa.append(line)
	return mapa

def posicao_mapa(mapa,coordenada):
	line = []
	cont = 0
	for i in range(num_linhas):
		line = mapa[i]
		if coordenada in line:
			return cont * len(line) + line.index(coordenada)
		cont = cont + 1

def escreve_mapa(mapa):
	for i in range(num_linhas):
		print mapa[i]