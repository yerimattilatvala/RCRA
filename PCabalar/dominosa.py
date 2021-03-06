'''
***** Nombre : Yeray
***** Apellidos : Mendez Romero
***** Login : yeray.mendez
'''

import argparse
import sys
from functions import *


#INICIO DEL PROGRAMA
# Recibe argumentos de entrada
#---------------------------------------------------------------------------#
ap = argparse.ArgumentParser()
ap.add_argument( "-g", required=False)
ap.add_argument('filename', nargs='?')
args = vars(ap.parse_args()) #{'filename':'file'}
#---------------------------------------------------------------------------#
dominosaMatrix = None
try:
    file = open(args['filename'],'r')
    dominosaMatrix = formatElements(file)
except ValueError as errv:
    print('**** Error trying to format -> '+errv.args[0])
    sys.exit()
except IsADirectoryError as errd:
    print(errd)
    sys.exit()
except FileNotFoundError as errf:
    print(errf)
    sys.exit()
except Exception as erre:
    print(erre)
    sys.exit()

solveDominosa(dominosaMatrix) 