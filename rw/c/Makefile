# CC = gcc
CFLAGS = -Wall -g   
LDFLAGS = -lpthread 

OBJS = main.o buffer.o lightswitch.o reader.o writer.o 

all: main

main: $(OBJS)
	$(CXX) $(CFLAGS) -o main $(OBJS) $(LDFLAGS) 

clean: 
	rm -rf $(A2OBJS) main
