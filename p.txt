/* nqueens.c - Pedro Cabalar
 * Department of Computer Science, University of Corunna, Spain
 * 14/02/2018
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdarg.h>
#include <unistd.h>

int n; // size = number of rows = number of columns = number of queens

#define QUEEN(X,Y) ((X)*n+(Y)+1)

int clauses=0;
FILE *f;

// Diagonals move from left to right

void diagonalDown(int x,int y) {
  int i,j,a,b;
  fprintf(f,"c No two queens at down diagonal starting in %d\n",QUEEN(x,y));

  for (i=x,j=y;i<n && j<n ;i++,j++)
    for (a=i+1,b=j+1; a<n && b<n; a++,b++) {
      fprintf(f,"-%d -%d 0\n",QUEEN(i,j),QUEEN(a,b)); clauses++;
    }
}

void diagonalUp(int x,int y) {
  int i,j,a,b;
  fprintf(f,"c No two queens at up diagonal starting in %d\n",QUEEN(x,y));

  for (i=x,j=y;i>=0 && j<n ;i--,j++)
    for (a=i-1,b=j+1; a>=0 && b<n; a--,b++) {
      fprintf(f,"-%d -%d 0\n",QUEEN(i,j),QUEEN(a,b)); clauses++;
    }

}

int main (int argc,char *argv[]) {
  int i,j,k,c,v;
  char message[2048];
  char *grid;
  
  if (argc!=2) { printf("nqueens <size>\n"); exit(1); }
  n=atoi(argv[1]);
  
  unlink("clauses.txt");
  unlink("satfile.txt");
  unlink("result.txt");
  f=fopen("clauses.txt","w");
  
  fprintf(f,"c Each row has at least some queen\n");
  for (i=0;i<n;i++) {
    for (j=0;j<n;j++)
      fprintf(f,"%d ",QUEEN(i,j));
    fprintf(f,"0\n"); clauses++;
  }

  fprintf(f,"c No two queens at same row\n");
  for (i=0;i<n;i++)
    for (j=0;j<n-1;j++)
      for (k=j+1;k<n;k++) {
        fprintf(f,"-%d -%d 0\n",QUEEN(i,j),QUEEN(i,k));
	clauses++;
      }

  fprintf(f,"c No two queens at same column\n");
  for (j=0;j<n;j++)
    for (i=0;i<n-1;i++)
      for (k=i+1;k<n;k++) {
        fprintf(f,"-%d -%d 0\n",QUEEN(i,j),QUEEN(k,j));
	clauses++;
      }

  for (j=0;j<n-1;j++) diagonalDown(0,j);
  for (i=1;i<n-1;i++) diagonalDown(i,0);
  for (j=0;j<n-1;j++) diagonalUp(n-1,j);
  for (i=1;i<n-1;i++) diagonalUp(i,0);
  
  fclose(f);
  f=fopen("satfile.txt","w");
  fprintf(f,"p cnf %d %d\n", n*n, clauses);
  fclose(f);
  system("cat clauses.txt >> satfile.txt\n");
  system("clasp --verbose=0 satfile.txt > result.txt\n");

  grid=(char *)calloc(n*n,sizeof(char));
  f=fopen("result.txt","r");
  while ((c=fgetc(f))!=EOF) {
    switch(c) {
      case 's':
	fscanf(f,"%s\n",message);
	if (strcmp("UNSATISFIABLE",message)==0) {
          printf("No solution\n"); exit(0);
        };
	break;
      case 'v':
	while ((c=fscanf(f,"%d",&v))==1) {
	  if (v>0) grid[v-1]=1;
	}
    }
  }
 
  for (i=0;i<n;i++) {
    for (j=0;j<n;j++)
      printf("%c ",(grid[QUEEN(i,j)-1]?'Q':'.'));
    printf("\n");
  }
  fclose(f);
  free(grid);
  
  return 0;
}
