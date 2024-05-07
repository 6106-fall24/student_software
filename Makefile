# The sources we're building - Optimized
HEADERS = $(wildcard *.h)
PRODUCT_SOURCES = $(wildcard *.c)

PRODUCT_OBJECTS = $(PRODUCT_SOURCES:.c=.o)

PRODUCT = test_program

DEFINES += -DSIMDE_ENABLE_NATIVE_ALIASES

# What we're building with
CC = clang-6106
CFLAGS = -std=gnu11 -Wall -Wno-psabi -fopencilk $(DEFINES)
LDFLAGS = -static -pthread -fuse-ld=lld -lrt -lm -fopencilk -flto 

include ./cilkutils.mk

# Determine which profile--debug or release--we should build against, and set
# CFLAGS appropriately.

ASAN ?= 0
ifneq ($(ASAN), 0)
	CFLAGS += -fsanitize=address 
	LDFLAGS += -fsanitize=address
endif

DEBUG ?= 0
ifeq ($(DEBUG), 1)
  # We want debug mode.
  CFLAGS += -g -O0 -gdwarf-3 -DDEBUG -fno-inline-functions -march=native 
else
  # We want release mode.
  CFLAGS += -O3 -DNDEBUG -ftree-vectorize -flto=full -march=native
endif

STRICT_CFLAGS = -Werror -Wpedantic

# By default, make the product.
.PHONY: all
all:		$(PRODUCT)

# How to clean up
.PHONY: clean
clean:
	$(RM) *.o test_program


# How to compile a C file
%.o:	%.c $(OPTIMIZED_HEADERS)
	$(CC) $(CFLAGS) $(EXTRA_CFLAGS) -o $@ -c $<

# How to link the product
# linking with X11 since that is used in project 2s
$(PRODUCT): LDFLAGS += -lXext -lX11
$(PRODUCT): CFLAGS += $(STRICT_CFLAGS)
$(PRODUCT):	$(PRODUCT_OBJECTS)
	$(CC) $(LDFLAGS) $(EXTRA_LDFLAGS) -o $@ $(PRODUCT_OBJECTS)
