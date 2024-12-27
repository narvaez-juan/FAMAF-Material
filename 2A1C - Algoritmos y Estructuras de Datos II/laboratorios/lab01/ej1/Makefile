CC = gcc
CFLAGS = -Wall -Werror -Wextra -pedantic -std=c99 -g
SOURCES = main.c
TARGET = reader

.PHONY: clean

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) -o $(TARGET) $< $(LFLAGS) $(LIBS)

clean:
	$(RM) $(TARGET)
