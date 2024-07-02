#ifndef _WEATHER_UTILS_H
#define _WEATHER_UTILS_H

#include "array_helpers.h"
#include "weather.h"

/* Read the lowest historical minimum temperature */
int lowest_historical_min_temp(WeatherTable a);

/* Read the highest maximum temperature for year */
void higher_max_temp_per_year(WeatherTable a, int output[YEARS]);

/* Read the highest monthly amount of precipitation */
void highest_monthly_precipitation(WeatherTable a, unsigned int output[YEARS]);

#endif