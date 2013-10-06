#include <stdio.h>
#include <stdlib.h>

int main() {
  int *leak = reinterpret_cast<int*>(malloc(sizeof(int)));
  fprintf(stderr, "In stderr.\n");
  fprintf(stdout, "In stdout.\n");
  return 18;
}
