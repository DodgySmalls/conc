# CC = gcc
CFLAGS = -Wall -g   
LDFLAGS = -lpthread 

OBJS = halt.o buffer.o operation.o

all: halt

halt: $(OBJS)
	$(CXX) $(CFLAGS) -o halt $(OBJS) $(LDFLAGS) 

clean: 
	rm -rf $(A2OBJS) main
