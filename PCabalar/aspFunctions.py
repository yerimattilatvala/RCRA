'''
***** Nombre : Yeray
***** Apellidos : Mendez Romero
***** Login : yeray.mendez
'''

import os

def writeElements(file):
    f = open('dominosa.txt','w')
    n = int(file.readline())    # lee el numero de elementos que deben de ser distintos si no puede formatearlo devuelve un ValueError que es capturado
    f.write('#const n='+str(n)+'.\n\n')
    f.write('value(0..'+str(n-1)+').\n')
    f.write('rows(0..'+str(n)+').\n')
    f.write('cols(0..'+str(n+1)+').\n\n')
    elem = 0
    rows = n-1
    cols = n
    i = -1
    for line in file.readlines():
        i += 1
        j = 0
        for x in line.split(): #reemplazar los espacios en blanco
            f.write('box('+str(i)+','+str(j)+','+ x+').\n')
            j += 1
            elem += 1
    f.write('\n')
    f.close()
    if elem != (n*(n+1)):
        os.remove('dominosa.txt')
        raise Exception('The number of elements is incorrect.')
        
        