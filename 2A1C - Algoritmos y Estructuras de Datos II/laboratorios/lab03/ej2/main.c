/*
  @file main.c
  @brief Defines main program function
*/

/* First, the standard lib includes, alphabetically ordered */
#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

/* Then, this project's includes, alphabetically ordered */
#include "array_helpers.h"
#include "weather_utils.h"

/**
 * @brief print usage help
 * @param[in] program_name Executable name
 */
void print_help(char *program_name) {
    /* Print the usage help of this program. */
    printf("Usage: %s <input file path>\n\n"
           "Load climate data from a given file in disk.\n"
           "\n"
           "The input file must exist in disk and every line in it must have the following format:\n\n"
           "<year> <month> <day> <temperature> <high> <low> <pressure> <moisture> <precipitations>\n\n"
           "Those elements must be integers and will be copied into the multidimensional integer array 'a'.\n"
           "The dimensions of the array are given by the macro tclimate.\n"
           "\n\n",
           program_name);
}

/**
 * @brief reads file path from command line
 *
 * @param[in] argc amount of command line arguments
 * @param[in] argv command line arguments
 *
 * @return An string containing read filepath
 */
char *parse_filepath(int argc, char *argv[]) {
    /* Parse the filepath given by command line argument. */
    char *result = NULL;

    if (argc < 2) {
        print_help(argv[0]);
        exit(EXIT_FAILURE);
    }

    result = argv[1];

    return (result);
}

/**
 * @brief Main program function
 *
 * @param[in] argc amount of command line arguments
 * @param[in] argv command line arguments
 *
 * @return EXIT_SUCCESS when programs executes correctly, EXIT_FAILURE otherwise
 */
int main(int argc, char *argv[]) {
    char *filepath = NULL;

    /* parse the filepath given in command line arguments */
    filepath = parse_filepath(argc, argv);

    /* create an array with the type of tclimate */
    WeatherTable array;

    /* parse the file to fill the array and obtain the actual length */
    array_from_file(array, filepath);

    /* show the ordered array in the screen */
    array_dump(array);

    /* Print the lowest historical minimum temperature */
    int lowest_min = lowest_historical_min_temp(array);
    printf("\n\nThe lowest historical minimum temperature is: %i\n\n", lowest_min);

    /* Print highest maximum temperature for every year */
    int highest_max_temp_year[YEARS];
    higher_max_temp_per_year(array, highest_max_temp_year);
    for (unsigned int years = 0u; years < YEARS; years++) {
        printf("The highest maximum temperature in %u is: %i\n",
                years + FST_YEAR, highest_max_temp_year[years]);
    }
    printf("\n");

    /* Print highest maximum precipitation month for every year */
    unsigned int highest_monthly_precipitations[YEARS];
    highest_monthly_precipitation(array, highest_monthly_precipitations);
    for (unsigned int years = 0u; years < YEARS; years++) {
        printf("The highest maximum precipitation month in %u is: %i\n",
                years + FST_YEAR, (month_t) highest_monthly_precipitations[years] + 1);
    }
    printf("\n");

    return (EXIT_SUCCESS);
}
