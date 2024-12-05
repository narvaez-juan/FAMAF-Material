/*
  @file array_helpers.c
  @brief Array Helpers method implementation
*/
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include "array_helpers.h"
#include "ansicolors.h"

#define ANSI_GRID ANSI_CYAN
#define ANSI_PLAYER ANSI_BRWHITE
#define ANSI_NORMAL ANSI_WHITE

static void draw_column_coords(void) {
    printf(ANSI_NORMAL " ");
    for (unsigned int col=0; col < COLUMNS; col++) {
        printf("   %u", col + FST_COLUMN);
    }
    printf("\n");
}

static void draw_row_coord(unsigned int row) {
    printf(ANSI_NORMAL
           "%c ", row + FST_ROW);
}

static void draw_separator(void) {
    printf(ANSI_GRID "--");
    for (unsigned int col = 0u; col < COLUMNS; ++col) {
        printf(ANSI_GRID "+---");
    }
    printf("+\n");
}

void board_draw(Board board, player_t player, unsigned int round) {
    assert(player < PLAYERS);
    printf(ANSI_PLAYER
           "Player %d:\n"
           "=========\n\n", player + FST_PLAYER);
    draw_column_coords();
    draw_separator();
    for (unsigned int row = 0u; row < ROWS ; ++row) {
        draw_row_coord(row);
        printf(ANSI_GRID "| ");
        for (unsigned int col = 0u; col < COLUMNS; ++col) {
            cell_draw(board[row][col][player], round);
            printf(ANSI_GRID " | ");
        }
        printf("\n");
        draw_separator();
    }
    printf("\n\n");
}

void array_dump(Board board) {
    for (unsigned int row = 0u; row < ROWS ; ++row) {
        for (unsigned int col = 0u; col < COLUMNS; ++col) {
            for (player_t player=player1; player < PLAYERS; ++player) {
                printf("(%c, %2u) player%d: ", row + FST_ROW, 
                                               col + FST_COLUMN,
                                               player + FST_PLAYER);
                cell_dump(board[row][col][player]);
                printf("\n");
            }
        }
        printf("\n");
    }
}

unsigned int get_points(Board board, player_t player, unsigned int round) {
    unsigned int points = 0u;
    player_t opponent = (player == player1) ? player2 : player1;
    for (unsigned int row = 0; row < ROWS; row++) {
        for (unsigned int col = 0; col < COLUMNS; col++) {
            cell_t cell = board[row][col][opponent];
            // Check if the opponent's cell was hit and within the specified round
            if (cell.status == hit && cell.round <= round) {
                if (cell.content == ship) {
                    points += 100;  // Each hit on opponent's ship is worth 100 points
                }
            }
        }
    }
    return points;
}




static unsigned int max(unsigned int x, unsigned int y) {
    return x >= y ? x: y;
}

unsigned int array_from_file(Board board, const char *filepath) {
    FILE *file = NULL;

    file = fopen(filepath, "r");
    if (file == NULL) {
        fprintf(stderr, "File does not exist.\n");
        exit(EXIT_FAILURE);
    }

    char s_row = 0;                         // To store the readed symbol for row, 'A', 'B', ...
    unsigned int k_column = 0u;             // To store readed unsigned integer for column
    unsigned int check_filelines=0u; 
    unsigned int max_round=0u;              // Maximun round encountered
    while (!feof(file)) {
        int res = fscanf(file, "(%c, %u) " , &s_row, &k_column);
        if (res != 2) {
            fprintf(stderr, "Error reading coordinates at line %u.\n", 
                    check_filelines + 1);
            exit(EXIT_FAILURE);
        }
        unsigned int row;
        unsigned int column;
        row = s_row - FST_ROW;
        column = k_column - FST_COLUMN;

        // Read data for first player cell
        cell_t player1_cell = cell_from_file(file);
        // Read data for second player cell
        cell_t player2_cell = cell_from_file(file);

        // Store data of both players in array
        board[row][column][player1] = player1_cell;
        board[row][column][player2] = player2_cell;

        // Update maximun round
        max_round = max(max_round, player1_cell.round);
        max_round = max(max_round, player2_cell.round);

        // Count readed lines
        check_filelines++;
    }
    if (check_filelines != MAX_COORDS) {
        fprintf(stderr, "Error: File does not contain the expected number of lines.\n");
        exit(EXIT_FAILURE);
    }
    fclose(file);
    return max_round;
}
