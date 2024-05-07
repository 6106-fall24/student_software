/**
 * Copyright (c) 2012-2019 the Massachusetts Institute of Technology
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 **/
#ifndef INCLUDED_CILKTOOL_DOT_H
#define INCLUDED_CILKTOOL_DOT_H
#include <inttypes.h>
typedef struct __cilkrts_stack_frame __cilkrts_stack_frame;

#ifdef __cplusplus
#define EXTERN_C extern "C" {
#define EXTERN_C_END }
#else
#define EXTERN_C
#define EXTERN_C_END
#endif

EXTERN_C
void cv_start(void);
void cv_stop(void);
void print_total(void);

void cilk_enter_begin(uint32_t prop, __cilkrts_stack_frame* sf, void* this_fn,
                      void* rip);
void cilk_enter_helper_begin(__cilkrts_stack_frame* sf, void* this_fn,
                             void* rip);
void cilk_enter_end(__cilkrts_stack_frame* sf, void* rsp);
void cilk_spawn_prepare(__cilkrts_stack_frame* sf);
void cilk_spawn_or_continue(int in_continuation);
void cilk_detach_begin(__cilkrts_stack_frame* parent);
void cilk_detach_end(void);
void cilk_sync_begin(__cilkrts_stack_frame* sf);
void cilk_sync_end(__cilkrts_stack_frame* sf);
void cilk_leave_begin(__cilkrts_stack_frame* sf);
void cilk_leave_end(void);

EXTERN_C_END

#endif  // INCLUDED_CILKTOOL_DOT_H
