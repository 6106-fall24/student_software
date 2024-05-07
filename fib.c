#include "fib.h"

#include <cilk/cilk.h>
#include <stdio.h>

#include "cilktool.h"

int fib(int n) {
  if (n < 2) {
    return n;
  }
  int x = cilk_spawn fib(n - 1);
  int y = fib(n - 2);
  cilk_sync;
  return x + y;
}

int fib_scope(int n) {
  if (n < 2) return n;  // base case
  int x, y;
  cilk_scope {                        // begin lexical scope of parallel region
    x = cilk_spawn fib_scope(n - 1);  // don't wait for function to return
    y = fib_scope(n - 2);  // may run in parallel with spawned function
  }                        // wait for spawned function if needed
  return x + y;
}
