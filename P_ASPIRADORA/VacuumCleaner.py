'''
***** Nombre : Yeray
***** Apellidos : Mendez Romero
***** Login : yeray.mendez
'''

import argparse
import sys
import subprocess

# Argumentos de entrada
ap = argparse.ArgumentParser()
ap.add_argument( "-g", required=False)
ap.add_argument('filename', nargs='?')
args = vars(ap.parse_args()) #{'filename':'file'}

# Formateamos el fichero roomX.txt para establecer el escenario
file = open(args['filename'],'r')

# distyRoom.txt contendra la descripicion del escenario
file2= open("dirtyRoom.txt","w")
c = -1
j = 0
rows = 0
contain = ''

for line in file.readlines():
    c +=1
    j =0
    rows += 1
    for x in line:
        for item in x.split():
            if item != '\n':
                if item =='@':
                    contain += 'position('+str(c)+','+str(j)+',0).\n'
                elif item == '#':
                    contain += 'obstacule('+str(c)+','+str(j)+').\n'
                elif item == 'X':
                    contain += 'goal('+str(c)+','+str(j)+').\n'
                j+=1
  
file.close()

# Escribimos los datos necesarios en el fichero dirtyRoom.txt
file2.write('#const columns = '+str(j)+'.\n')
file2.write('#const rows = '+str(rows)+'.\n')
file2.write(contain)
file2.close()

# Llamamos a clingo con el fichero de reglas y el dirtyRoom.txt y guardamos la salida en el fichero output.txt
result = open('output.txt','w')
content = subprocess.Popen(["clingo", "cleaner.txt","dirtyRoom.txt"], stdout=subprocess.PIPE)
result.write(content.stdout.read().decode("utf-8"))
result.close()

# Finalmente leemos el fichero output.txt y guardamos los movimientos realizados en vacuumCleanerSolution.txt
file = open('output.txt','r')
file2 = open('vacuumCleanerSolution.txt','w')
for line in file.readlines():
    for x in line.split():
        if x[0:len(x)-5] == 'move' or x[0:len(x)-5] == 'move(':
            file2.write(x+'\n')

file.close()
file2.close()