'''
***** Nombre : Yeray
***** Apellidos : Mendez Romero
***** Login : yeray.mendez
'''

import argparse
import sys
import subprocess


#INICIO DEL PROGRAMA
# Recibe argumentos de entrada
#---------------------------------------------------------------------------#
ap = argparse.ArgumentParser()
ap.add_argument( "-g", required=False)
ap.add_argument('filename', nargs='?')
args = vars(ap.parse_args()) #{'filename':'file'}
#---------------------------------------------------------------------------#
file = open(args['filename'],'r')
file2= open("dirtyRoom.txt","w")
c = -1;
j = 0;
filas = 0;
contenido = ''

for line in file.readlines():
    c +=1
    j =0
    filas += 1
    for x in line:
        for item in x.split():
            if item != '\n':
                if item =='@':
                    contenido += 'pos('+str(c)+','+str(j)+',0).\n'
                elif item == '#':
                    contenido += 'obstaculo('+str(c)+','+str(j)+').\n'
                elif item == 'X':
                    contenido += 'meta('+str(c)+','+str(j)+').\n'
                j+=1
  
file.close()
    
file2.write('#const c = '+str(j)+'.\n')
file2.write('#const f = '+str(filas)+'.\n')
file2.write(contenido)
file2.close()
