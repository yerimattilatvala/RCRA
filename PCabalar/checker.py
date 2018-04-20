#!/usr/bin/env python
import sys

def openfile(fname):
    try:
        file=open(fname,"r")
    except:
        sys.exit("Error: file %s not found or could not be opened." % fname)
    return file

if len(sys.argv)!=3:
    sys.exit("checker <domainfile> <solutionfile>")

input=openfile(sys.argv[1])
solution=openfile(sys.argv[2])

# Store the input number in array num
line=input.readline()
n=int(line)
num=[]
for line in input:
    numbers=line.split()
    l=[]
    for v in numbers:
        l.append(int(v))
    num.append(l)
    
# Store the arrows in array dir
dir=[]
for line in solution:
    l=[]
    for v in line[:-1]:
        l.append(v)
    dir.append(l)

# Store all tiles in a list of pairs
tiles={}
for i in range(n):
    for j in range(i,n):
        tiles[(i,j)]=-1
        
for i in range(n):
    for j in range(n+1):
        if dir[i][j]=='>' or dir[i][j]=='v':
            if dir[i][j]=='>':
                if j==n or dir[i][j+1]!='<':
                    sys.exit("Error (row %d, column %d): unmatched '>'" % (i,j))
                x,y=num[i][j],num[i][j+1]
            elif dir[i][j]=='v':
                if i==n-1 or dir[i+1][j]!='^':
                    sys.exit("Error (row %d, column %d): unmatched 'v'" % (i,j))
                x,y=num[i][j],num[i+1][j]                    
            if x>y:
                x,y=y,x
            if tiles[(x,y)]>=0:
                sys.exit("Error (row %d, column %d): tile (%d,%d) also occurs at row %d, column %d" % (i,j,x,y,tiles[(x,y)]//(n+1),tiles[(x,y)] % (n+1)))
            tiles[(x,y)]=i*(n+1)+j

for t in tiles:
    if tiles[t]<0:
        sys.exit("Error: tile %s does not occur" % (t,))
        
print("Correct solution!")
