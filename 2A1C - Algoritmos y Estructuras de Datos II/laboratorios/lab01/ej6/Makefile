CC = gcc
CFLAGS = -Wall -Werror -Wextra -pedantic -std=c99 -g
SOURCES = array_helpers.c main.c
OBJECTS = $(SOURCES:.c=.o)
TARGET = reader

.PHONY: clean

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) -o $(TARGET) $(LFLAGS) $(LIBS)

.c.o:
	$(CC) $(CFLAGS) -c $< 

clean:
	$(RM) $(OBJECTS) $(TARGET)
