#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#define ARRAY_SIZE 4

struct bound_data {
    bool is_upperbound;
    bool is_lowerbound;
    bool exists;
    unsigned int where;
};

struct bound_data check_bound(int value, int arr[], unsigned int length) {
    struct bound_data res;
    int upper = arr[0];
    int lower = arr[0];
    unsigned int i = 0;
    
    res.is_upperbound = false;
    res.is_lowerbound = false;
    res.exists = false;
    res.where = 0;
    
    while (i < length)
    {
    	if (arr[i] > upper)
    	{
    		upper = arr[i];
    	}
    	if (arr[i] < lower)
    	{
    		lower = arr[i];
    	} 
    	if (arr[i] == value)
    	{
    		res.exists = true;
    		res.where = i;
    	}
    	i++;
    }
    
    res.is_upperbound = value >= upper;
    res.is_lowerbound = value <= lower;
    
    return res;
}

int main(void) {
    int a[ARRAY_SIZE] = {0, -1, 9, 4};
    int value=9;
    
    int i = 0;
    while (i < ARRAY_SIZE)
    {
    	printf("Inserte valor para a[%d]: ", i);
    	scanf("%d", &a[i]);
    	i++;
    }
    
    struct bound_data result = check_bound(value, a, ARRAY_SIZE);

    printf("%d\n", result.is_upperbound); 
    printf("%d\n", result.is_lowerbound); 
    printf("%u\n", result.exists);        
    printf("%u\n", result.where);         

    return EXIT_SUCCESS;
}

