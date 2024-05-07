#include "main.h"

#include <cilk/cilk.h>
#include <stdio.h>
#include <stdlib.h>

#include "cilktool.h"
#include "fib.h"
#include "sum.h"

static int multisum(int* a, int* b, int* c, int* d) {
  *a = cilk_spawn sum(1, 2);
  *b = cilk_spawn sum(3, 4);
  *c = sum(5, 6);
  *d = sum(7, 8);
  cilk_sync;
  return *a + *b + *c + *d;
}

int main(void) {
  int a, b, c, d;
  int m = multisum(&a, &b, &c, &d);
  if (m != 1 + 2 + 3 + 4 + 5 + 6 + 7 + 8) {
    printf("Sum Test failed!!!: a=%d, b=%d, c=%d, d=%d", a, b, c, d);
    return 1;
  }
  int f = fib(10);
  int f_scope = fib_scope(10);
  if (f != 55) {
    printf("Fib Test failed!!!: fib()=%d", f);
    return 1;
  }
  if (f_scope != 55) {
    printf("Fib Test failed!!!: fib_scope()=%d", f_scope);
    return 1;
  }
  int x[48], y[48], z[48];
  for (int i = 0; i < 48; i++) {
    x[i] = 3 * i + 1;
    y[i] = 2 * i - 3;
  }
  sum_vector(x, y, z, 48);
  for (int i = 0; i < 48; i++) {
    if (z[i] != 5 * i - 2) {
      printf("Vector Test failed!!!: i=%d, x=%d, y=%d, z=%d", i, x[i], y[i], z[i]);
      return 1;
    }
  }

  printf("Welcome to 6.106!\n");
  return 0;
}
