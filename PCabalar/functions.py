'''
***** Nombre : Yeray
***** Apellidos : Mendez Romero
***** Login : yeray.mendez
'''

import numpy as np
import sys 
import subprocess

variableNumber = 0  # Contador que determina la variable de cada ficha para el fichero DIMACS
Count = 0           # Contador almacena el número de cláusulas para el fichero DIMACS
Visited = []        # Lista que almacena las fichas que ya han sido visitadas
Variables = []      # Lista que almacena elementos que contienen las coordenadas de cada ficha de la matriz y su variable
CurrentVariables = []   # lista que almacena las variables de cada ficha/s encontradas en una interacción del bucle de la función dominosa
VerticalFreePos = []    # Lista que almacena las coordenadas verticales no visitadas
HorizontalFreePos = []  # Lista que almacena las coordenadas horizontales no visitadas
indexVert = []          # Lista con los indices de los elementos de la lista VerticalFreePos que hay que eliminar tras realizar una busqueda en vertical
indexHor = []           # Lista con los indices de los elementos de la lista HorizontalFreePos que hay que eliminar tras realizar una busqueda en vertical

'''
Función que elemina los elementos de list indicados en la
lista de indices index.
'''
def deleteIndex(list,index):
    if len(index):
        for x in index:
            index[:] = [y -1 for y in index]
        del index[:]

'''
Función que inicializa las coordenadas libres en las 
listas HorizontalFreePos y VerticalFreePos.
'''
def getFreePositions(matrix):
    rows = matrix.shape[0]
    cols = matrix.shape[1]
    for x in range(rows):
        for y in range(cols):
            if x != rows-1:
                VerticalFreePos.append(((x,y),(x+1,y)))
            if y != cols-1:
                HorizontalFreePos.append(((x,y),(x,y+1)))
                

'''
Funcion que formatea el fichero de entrada
a una matriz numérica sobre la que iterar.
'''
def formatElements(file):
    n = int(file.readline())   
    lista = []
    for line in file.readlines():
        for x in line.split():
            if x != '\n':   
                lista.append(int(x))
    if (len(lista)) != (n*(n+1)):
        raise Exception('The number of elements is incorrect.')
    else:
        dominosaMatrix = np.array(lista).reshape(n,n+1)
        getFreePositions(dominosaMatrix)
        return dominosaMatrix

def isVariableExists(x1,y1,x2,y2):
    exists = False
    for x in Variables:
        if (x1,y1) in x and (x2,y2) in x:
            exists = True
    return exists

def isElementVisited(n1,n2):
    visited = True
    if ((n1,n2) not in Visited) or ((n2,n1) not in Visited):
        visited =  False
    return visited

def insertElement(n1,n2):
    Visited.append((n1,n2))
    Visited.append((n2,n1))

'''
Funcion que para ficha, recorre HorizontalFreePos y busca fichas repetidas en sentido horizontal
'''
def searchHorizontalElements(n1,n2,matrix):
    global variableNumber
    for x in HorizontalFreePos:
        if ((matrix[x[0]],matrix[x[1]])==(n1,n2)) or ((matrix[x[0]],matrix[x[1]])==(n2,n1)):
            if not isVariableExists(x[0][0],x[0][1],x[1][0],x[1][1]):
                variableNumber += 1
                Variables.append(((x[0][0],x[0][1]),(x[1][0],x[1][1]),variableNumber))
                CurrentVariables.append(variableNumber)
                index = HorizontalFreePos.index(x)
                indexHor.append(index)
    deleteIndex(HorizontalFreePos,indexHor)

'''
Funcion que para ficha, recorre VerticalFreePos y busca fichas repetidas en sentido vertical
'''
def searchVerticalElements(n1,n2,matrix):
    global variableNumber
    for x in VerticalFreePos:
        if ((matrix[x[0]],matrix[x[1]])==(n1,n2)) or ((matrix[x[0]],matrix[x[1]])==(n2,n1)):
            if not isVariableExists(x[0][0],x[0][1],x[1][0],x[1][1]):
                variableNumber += 1
                Variables.append(((x[0][0],x[0][1]),(x[1][0],x[1][1]),variableNumber))
                CurrentVariables.append(variableNumber)
                index = VerticalFreePos.index(x) 
                indexVert.append(index)
    deleteIndex(VerticalFreePos,indexVert)

'''
writeNegativeVariables y writeVariables impiden que se haya
fichas repetidas escribiendo las implicaciones necesarias.
'''
def writeNegativeVariables(file,x):
    global Count
    for variable in CurrentVariables:
        if variable !=x:
            file.write('-'+str(x)+' -'+str(variable)+' 0\n')
            Count +=  1

def writeVariables(n1,n2,file):
    CurrentVariables.sort()
    file.write("c No hay dos fichas repetidas ("+str(n1)+","+str(n2)+") o ("+str(n2)+","+str(n1)+") .\n")
    global Count
    line = ''
    for x in CurrentVariables:
        line += str(x)+" "
        writeNegativeVariables(file,x)
    line += '0\n'
    file.write(line)
    Count +=  1

'''
obtainCrossVariables y noCross impide que una ficha se solape
con fichas adyacentes escribiendo las implicaciones necesarias.
'''
def obtainCrossVariables(x):
    global Count
    line = ""
    for t in Variables:
        if t[2]!=x[2]:
            if x[0] == t[0] or x[1] == t[0] or x[0] == t[1] or x[1] == t[1]:
                line+="-"+str(x[2])+" -"+str(t[2])+" 0\n"
                Count +=1
    #line+="0\n"
    return line

def noCross(file):
    f= open("satfile.cnf","w")
    #f.write("c Variables : \n")
    file.write("c No hay solapamiento entre fichas. \n")
    #f.write("c ")
    for x in Variables:
        #f.write(str(x[2])+" ")
        file.write(obtainCrossVariables(x))
    file.close()
    #f.write("\n")
    f.write("p cnf "+str(variableNumber)+" "+str(Count)+" \n")
    f1 = open("clauses.txt","r")
    for lineReaded in f1:
        f.write(lineReaded)
    f.close()
    f1.close()

def isSatisfiable(file):
    positiveVariables = []
    satisfiable = False
    for line in file.readlines():
        if line[0] == 'v':
            for term in line.split():
                if term !='v':
                    if int(term)>0:
                        positiveVariables.append(int(term))
        if line[0] == 's':
            my_line = line.split(' ', 1)[1]
            my_line = my_line[:len(my_line)-1]  
            if my_line == 'SATISFIABLE':
                satisfiable = True
    
    file.close()
    if satisfiable:
        return positiveVariables
    else:
        print('****UNSATISFIABLE****')
        print('Going out of the program...')
        sys.exit()

def returnCoords(x):
    for v in Variables:
        if x == v[2]:
            return(v[0],v[1])

'''
Función que recibe las variables necesarias de la salida
de clasp 0 satfil.cnf,la muestra por pantalla y la escribe en el
fichero file_result.txt.
'''
def writeSolution(list,rows,cols):
    charar = np.chararray((rows,cols))
    for x in list:
        c1,c2 = returnCoords(x)
        if c2[1] == c1[1]+1:
            charar[c1]='>'
            charar[c2]='<'
        elif c2[0] == c1[0]+1:
            charar[c1]='v'
            charar[c2]='^'
    line = ''
    i = 0
    charar.astype(str)
    file = open('file_result.txt','w')
    for (x,y),value in np.ndenumerate(charar):
        i+=1
        line+=value.decode('UTF-8')
        if i == cols:
            i=0
            line+='\n'
    print(line)
    file.write(line)
    file.close()

 #---------------------------------------------------------------#
''' 
 Función principal y que resuelve dominosa.
    - Su funcionamiento es el siguiente:
            - Para cada posible ficha, recorre la las listas VerticalFreePos y HorizontalFreePos
              para determinar las variables, coordenadas y fichas.
            - Una vez determinada el numero de fichas existentes de cada tipo, 
              escribe en el fichero DIMACS las implicaciones para que solo sea una de ellas validas.
            - Tras almacenar todas las variables del matriz, escribe en el fichero DIMACS las restricciones 
              que impiden que las fichas se solapen unas a otras.
            - Ejecuta clasp 0 satfile.cnf, obtiene su salida y la escribe en file_result.txt y la muestra por pantalla.
'''

def solveDominosa(matrix):
    global variableNumber
    rows = matrix.shape[0]
    cols = matrix.shape[1]
    f= open("clauses.txt","w")
    for (x,y),_ in np.ndenumerate(matrix):
            n1 = None
            n2 = None
            n3 = None
            n1 = matrix[x,y]
            if ( x < (rows-1)): 
                n3 = matrix[x+1,y]
            if (y < (cols-1)):
                n2 = matrix[x,y+1]
            if n1 is not None and n2 is not None:
                if not isElementVisited(n1,n2):
                    insertElement(n1,n2)
                    if not isVariableExists(x,y,x,y+1):
                        variableNumber +=1
                        index = HorizontalFreePos.index(((x,y),(x,y+1)))
                        del HorizontalFreePos[index]
                        Variables.append(((x,y),(x,y+1),variableNumber)) 
                        CurrentVariables.append(variableNumber)  
                        searchHorizontalElements(n1,n2,matrix)
                        searchVerticalElements(n1,n2,matrix)
                        writeVariables(n1,n2,f)
                        del CurrentVariables[:]
                else: 
                    index = HorizontalFreePos.index(((x,y),(x,y+1)))
                    del HorizontalFreePos[index]
            if n1 is not None and n3 is not None:
                if not isElementVisited(n1,n3):
                    insertElement(n1,n3)
                    if not isVariableExists(x,y,x+1,y):
                        variableNumber +=1
                        index = VerticalFreePos.index(((x,y),(x+1,y)))
                        del VerticalFreePos[index]
                        Variables.append(((x,y),(x+1,y),variableNumber)) 
                        CurrentVariables.append(variableNumber)
                        searchHorizontalElements(n1,n3,matrix)
                        searchVerticalElements(n1,n3,matrix)
                        writeVariables(n1,n3,f)
                        del CurrentVariables[:]
                else:
                    index = VerticalFreePos.index(((x,y),(x+1,y)))
                    del VerticalFreePos[index]
    noCross(f)
    result = open('result.txt','w')
    content = subprocess.Popen(["clasp", "satfile.cnf"], stdout=subprocess.PIPE)
    result.write(content.stdout.read().decode("utf-8"))
    result.close()
    result = open('result.txt','r')
    variables = isSatisfiable(result)
    variables.sort()
    writeSolution(variables,rows,cols)