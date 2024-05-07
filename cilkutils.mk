ifeq ($(CILKSAN),1)
	CFLAGS += -fsanitize=cilk -DCILKSAN=1
	LDFLAGS += -fsanitize=cilk
else ifeq ($(CILKSCALE),1)
	CFLAGS += -fcilktool=cilkscale
	LDFLAGS += -fcilktool=cilkscale
endif
