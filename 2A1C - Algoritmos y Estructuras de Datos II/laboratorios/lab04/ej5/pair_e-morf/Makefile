CC = gcc
CFLAGS = -Wall -Werror -Wextra -pedantic -std=c99 -g
SOURCES = pair.c main.c
TARGET = main

.PHONY: clean

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) $(SOURCES) -o $(TARGET) $(LFLAGS) $(LIBS)

clean:
	$(RM) $(TARGET)
