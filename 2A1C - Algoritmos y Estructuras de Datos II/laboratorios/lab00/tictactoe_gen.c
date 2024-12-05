#include <stdlib.h>  /* exit() y EXIT_FAILURE */
#include <stdio.h>   /* printf(), scanf()     */
#include <stdbool.h> /* Tipo bool             */

#include <assert.h>  /* assert() */

#define SIZE_BOARD 4

#define CELL_MAX (SIZE_BOARD * SIZE_BOARD - 1)

void print_sep(int length) {
    printf("\t ");
    for (int i=0; i < length;i++) printf("................");
    printf("\n");

}

void print_board(char board[SIZE_BOARD][SIZE_BOARD])
{
    int cell = 0;

    print_sep(SIZE_BOARD);
    for (int row = 0; row < SIZE_BOARD; ++row) {
        for (int column = 0; column < SIZE_BOARD; ++column) {
            printf("\t | %d: %c ", cell, board[row][column]);
            ++cell;
        }
        printf("\t | \n");
        print_sep(SIZE_BOARD);
    }
}

bool check_row(char board[SIZE_BOARD][SIZE_BOARD], int ROW)
{
    bool there_is_a_row = false;
    char row_Rc = board[ROW][0];

    for (int col = 0; col < SIZE_BOARD; ++col)
    {
        there_is_a_row = row_Rc == board[ROW][col];
        row_Rc = board[ROW][col];

        if (!there_is_a_row || row_Rc == '-')
        {
            there_is_a_row = false;
            break;
        }
    }

    return there_is_a_row;
}

bool check_col(char board[SIZE_BOARD][SIZE_BOARD], int COL)
{
    bool there_is_a_col = false;
    char row_rC = board[0][COL];

    for (int row = 0; row < SIZE_BOARD; ++row)
    {
        there_is_a_col = row_rC == board[row][COL];
        row_rC = board[row][COL];

        if (!there_is_a_col || row_rC == '-')
        {
            there_is_a_col = false;
            break;
        }
    }

    return there_is_a_col;
}

bool check_diag1(char board[SIZE_BOARD][SIZE_BOARD])
{
    bool there_is_a_diag1 = false;
    char cell_ii = board[0][0];

    for (int i = 0; i < SIZE_BOARD; ++i)
    {
        there_is_a_diag1 = cell_ii == board[i][i];
        cell_ii = board[i][i];

        if (!there_is_a_diag1 || cell_ii == '-')
        {
            there_is_a_diag1 = false;
            break;
        }
    }

    return there_is_a_diag1;
}

bool check_diag2(char board[SIZE_BOARD][SIZE_BOARD])
{
    bool there_is_a_diag2 = false;
    char cell_im = board[0][SIZE_BOARD - 1];

    for (int i = 0; i < SIZE_BOARD; ++i)
    {
        there_is_a_diag2 = cell_im == board[i][SIZE_BOARD - 1 - i];
        cell_im = board[i][SIZE_BOARD - 1 - i];

        if (!there_is_a_diag2 || cell_im == '-')
        {
            there_is_a_diag2 = false;
            break;
        }
    }

    return there_is_a_diag2;
}

char get_winner(char board[SIZE_BOARD][SIZE_BOARD])
{
    char winner = '-';

    for (int x = 0; x < SIZE_BOARD; ++x) {

        if (check_row(board, x))
        {
            winner = board[x][0];
        }
        else if (check_col(board, x))
        {
            winner = board[0][x];
        }
    }

    if (check_diag1(board))
    {
        winner = board[0][0];
    }
    else if (check_diag2(board))
    {
        winner = board[0][SIZE_BOARD - 1];
    }
    
    return winner;
}

bool has_free_cell(char board[SIZE_BOARD][SIZE_BOARD])
{
    bool free_cell=false;
    	
    	for (int row = 0; row < SIZE_BOARD; ++row) {
        	for (int column = 0; column < SIZE_BOARD; ++column) {
    			if (board[row][column] == '-')
    			{
    				free_cell = true;
    				break;
    			}
    		}
    		if (free_cell)
    		{
    			break;
    		}
    	}
    
    return free_cell;
}

int main(void)
{
    printf("TicTacToe [InCoMpLeTo :'(]\n");

    char board[SIZE_BOARD][SIZE_BOARD];

    for (int i = 0; i < SIZE_BOARD; ++i)
    {
        for (int j = 0; j < SIZE_BOARD; ++j)
        {
            board[i][j] = '-';
        }
    }

    char turn = 'X';
    char winner = '-';
    int cell = 0;
    while (winner == '-' && has_free_cell(board)) {
        print_board(board);
        printf("\nTurno %c - Elija posición (número del 0 al %d): ", turn,
               CELL_MAX);
        int scanf_result = scanf("%d", &cell);
        if (scanf_result <= 0) {
            printf("Error al leer un número desde teclado\n");
            exit(EXIT_FAILURE);
        }
        if (cell >= 0 && cell <= CELL_MAX) {
            int row = cell / SIZE_BOARD;
            int colum = cell % SIZE_BOARD;
            if (board[row][colum] == '-') {
                board[row][colum] = turn;
                turn = turn == 'X' ? 'O' : 'X';
                winner = get_winner(board);
            } else {
                printf("\nCelda ocupada!\n");
            }
        } else {
            printf("\nCelda inválida!\n");
        }
    }
    print_board(board);
    if (winner == '-') {
        printf("Empate!\n");
    } else {
        printf("Ganó %c\n", winner);
    }
    return 0;
}
