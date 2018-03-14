import numpy as np
import sys 
import subprocess

Count = 0
Visited = []
Variables = []
CurrentVariables = []

def mappingPos(row,col,colsMatrix):
    atom = (row*colsMatrix) + (col+1)
    return atom

def posCoord(n,cols):
    for x in range(cols-1):
        for y in range(cols):
            if n == mappingPos(x,y,cols):
                return x,y 

def formatElements(file):
    n = int(file.readline())    # lee el numero de elementos que deben de ser distintos si no puede formatearlo devuelve un ValueError que es capturado
    lista = []
    for line in file.readlines():
        for x in line.split(): #reemplazar los espacios en blanco
            if x != '\n':   # no tiene en cuenta los saltos de linea
                lista.append(int(x))
    if (len(lista)) != (n*(n+1)):
        raise Exception('The number of elements is incorrect.')
    else:
        dominosaMatrix = np.array(lista).reshape(n,n+1)
        return dominosaMatrix

def isVariableExists(x):
    exists = False
    if x in Variables:
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

def searchHorizontalElements(n1,n2,matrix):
        rowsMatrix = matrix.shape[0]
        colsMatrix = matrix.shape[1]
        for x in range(rowsMatrix):
            for y in range(colsMatrix):
                if y != (colsMatrix-1):
                    if ((matrix[x,y],matrix[x,y+1])==(n1,n2)) or ((matrix[x,y],matrix[x,y+1])==(n2,n1)):
                        x1 = mappingPos(x,y,colsMatrix)
                        x2 = mappingPos(x,y+1,colsMatrix)
                        x1x2 = int(str(x1) + str(x2))
                        if  not isVariableExists(x1x2):
                            Variables.append(x1x2) 
                            CurrentVariables.append(x1x2)    

def searchVerticalElements(n1,n2,matrix):
        rowsMatrix = matrix.shape[0]
        colsMatrix = matrix.shape[1]
        for y in range(colsMatrix):
            for x in range(rowsMatrix):
                if x!=rowsMatrix-1:
                    if ((matrix[x,y],matrix[x+1,y])==(n1,n2)) or ((matrix[x,y],matrix[x+1,y])==(n2,n1)):
                        x1 = mappingPos(x,y,colsMatrix)
                        x2 = mappingPos(x+1,y,colsMatrix)
                        x1x2 = int(str(x1) + str(x2))
                        if  not isVariableExists(x1x2):
                                Variables.append(x1x2) 
                                CurrentVariables.append(x1x2) 

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

def obtainCrossVariables(x):
    global Count
    line = ""
    number = str(x)
    #line +="-"+number+" "
    l = len(number)
    n1 = int(number[:int(l/2)])
    n2 = int(number[int(l/2):])
    for t in Variables:
        if t!=x:
            numbert = str(t)
            lt = len(numbert)
            n3 = int(numbert[:int(lt/2)]) 
            n4 = int(numbert[int(lt/2):]) 
            if n1 == n3 or n2 == n3 or n2 == n4 or n1 == n4:
                line+="-"+number+" -"+numbert+" 0\n"
                Count +=1
    #line+="0\n"
    return line

def noCross(file):
    global Count
    clauses = 0
    f= open("satfile.cnf","w")
    Variables.sort()
    f.write("c Variables : \n")
    file.write("c No hay solapamiento entre fichas. \n")
    f.write("c ")
    for x in Variables:
        f.write(str(x)+" ")
        file.write(obtainCrossVariables(x))
    file.close()
    f.write("\n")
    f.write("p cnf "+str(max(Variables))+" "+str(Count)+" \n")
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
            print(my_line)
            if my_line == 'SATISFIABLE':
                satisfiable = True
    
    file.close()
    if satisfiable:
        print('Problem Solved')
        return positiveVariables
    else:
        print('****UNSATISFIABLE****')
        print('Going out of the program...')
        sys.exit()

def writeSolution(list,rows,cols):
    charar = np.chararray((rows,cols))
    for x in list:
        numbert = str(x)
        lt = len(numbert)
        n1 = int(numbert[:int(lt/2)]) 
        n2 = int(numbert[int(lt/2):])
        if n2 == n1+1:
            charar[posCoord(n1,cols)]='>'
            charar[posCoord(n2,cols)]='<'
        else:
            charar[posCoord(n1,cols)]='v'
            charar[posCoord(n2,cols)]='^'
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

        
def solveDominosa(matrix):
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
                    x1 = mappingPos(x,y,cols)
                    x2 = mappingPos(x,y+1,cols)
                    x1x2 = int(str(x1) + str(x2))
                    if  not isVariableExists(x1x2):
                        Variables.append(x1x2)
                        CurrentVariables.append(x1x2)
                    searchHorizontalElements(n1,n2,matrix)
                    searchVerticalElements(n1,n2,matrix)
                    #method que escribe convinacion variables
                    writeVariables(n1,n2,f)
                    del CurrentVariables[:]
            if n1 is not None and n3 is not None:
                if not isElementVisited(n1,n3):
                    insertElement(n1,n3)
                    x1 = mappingPos(x,y,cols)
                    x2 = mappingPos(x+1,y,cols)
                    x1x2 = int(str(x1) + str(x2))
                    if  not isVariableExists(x1x2):
                        Variables.append(x1x2)
                        CurrentVariables.append(x1x2)
                    searchHorizontalElements(n1,n3,matrix)
                    searchVerticalElements(n1,n3,matrix)
                    #method que escribe convinacion variables
                    writeVariables(n1,n3,f)
                    del CurrentVariables[:]
            #return 0
    noCross(f)
    result = open('result.txt','w')
    content = subprocess.run(["clasp", "satfile.cnf"], stdout=subprocess.PIPE)
    result.write(content.stdout.decode("utf-8"))
    result.close()
    result = open('result.txt','r')
    variables = isSatisfiable(result)
    variables.sort()
    writeSolution(variables,rows,cols)