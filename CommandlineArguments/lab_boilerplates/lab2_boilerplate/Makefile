CC=g++
CFLAGS=-g -Wall

OBJS=utilities_lab2.o main_lab2.o

all:
	echo "Specify an acitivity."

activity1: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o ShowArgs

activity2: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o Act2

activity3: $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o calc

clean:
	rm -f $(OBJS) lab2.out ShowArgs Act2 calc *.pyc
	rm -rf __pycache__

main_lab2.o: main_lab2.cc utilities_lab2.o
	$(CC) $(CFLAGS) -c main_lab2.cc

utilities_lab2.o: utilities_lab2.cc definitions_lab2.h
	$(CC) $(CFLAGS) -c utilities_lab2.cc

tar:
	tar -cf lab2.tar main_lab2.cc utilities_lab2.cc definitions_lab2.h
