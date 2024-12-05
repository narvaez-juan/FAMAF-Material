#include "array_helpers.h"
#include "weather_utils.h"


int lowest_historical_min_temp(WeatherTable a)
{
    int lowest_min = 1000;

    for (unsigned int year = 0u; year < YEARS; ++year) {
        for (month_t month = january; month <= december; ++month) {
            for (unsigned int day = 0u; day < DAYS; ++day) {
                if (a[year][month][day]._min_temp < lowest_min){
                    lowest_min = a[year][month][day]._min_temp;
                }
            }
        }
    }

    return lowest_min;
}


void higher_max_temp_per_year(WeatherTable a, int output[YEARS]) {
    
    int higher_max_tyear = -1000;

    for (unsigned int year = 0u; year < YEARS; ++year) {
        for (month_t month = january; month <= december; ++month) {
            for (unsigned int day = 0u; day < DAYS; ++day) {
                if (a[year][month][day]._max_temp > higher_max_tyear) {
                    higher_max_tyear = a[year][month][day]._max_temp;
                }
            }
        }
        output[year] = higher_max_tyear;
        higher_max_tyear = -1000;
    }
}


void highest_monthly_precipitation(WeatherTable a, 
                                   unsigned int output[YEARS]) {
    unsigned int higher_monthly_prec = 0u;
    unsigned int tmp_higher_prec = 0u;
    unsigned int month_highest= 0u;

    for (unsigned int year = 0u; year < YEARS; ++year) {
        for (month_t month = january; month <= december; ++month) {
            for (unsigned int day = 0u; day < DAYS; ++day) {
                if (a[year][month][day]._rainfall > higher_monthly_prec) {
                    tmp_higher_prec = a[year][month][day]._rainfall;
                }
            }

            if (higher_monthly_prec < tmp_higher_prec) {
                higher_monthly_prec = tmp_higher_prec;
                month_highest = (unsigned int) month;
            }
            tmp_higher_prec = 0u;
        }
        output[year] = month_highest;
        month_highest = 0u;
        higher_monthly_prec = 0u;
    }
}
