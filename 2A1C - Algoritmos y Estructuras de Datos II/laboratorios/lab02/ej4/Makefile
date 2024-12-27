CC = gcc
CFLAGS = -Wall -Werror -Wextra -pedantic -std=c99 -g
NO_PIE = -no-pie
SOURCES = array_helpers.c sort.c main.c
OBJECTS = $(SOURCES:.c=.o)
ALL_OBJECTS = $(OBJECTS) sort_helpers.o 
TARGET = sorter

.PHONY: clean

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) $(NO_PIE) $(ALL_OBJECTS) -o $(TARGET) $(LFLAGS) $(LIBS)

.c.o:
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	$(RM) $(OBJECTS) $(TARGET)
