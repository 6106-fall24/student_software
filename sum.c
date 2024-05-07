#include <x86/avx2.h>
#include "sum.h"

int sum(int a, int b) { return a + b; }

void sum_vector(int *a, int *b, int *c, int n) {
  int i;
  for (i = 0; i + 8 <= n; i += 8) {
    __m256i va = _mm256_loadu_si256((__m256i*) (a + i));
    __m256i vb = _mm256_loadu_si256((__m256i*) (b + i));
    __m256i vc = _mm256_add_epi32(va, vb);
    _mm256_storeu_si256((__m256i*) (c + i), vc);
  }

  for ( ; i < n; i++) {
    c[i] = sum(a[i], b[i]);
  }
}
