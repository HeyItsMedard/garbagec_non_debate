#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Function to simulate memory allocation and deallocation
void simulate_memory_ops(int num_objects) {
    int i;
    int **objects = (int **)malloc(num_objects * sizeof(int *));
    if (objects == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }

    // Allocate memory
    for (i = 0; i < num_objects; i++) {
        objects[i] = (int *)malloc(1000 * sizeof(int)); // Creating an array of 1000 integers
        if (objects[i] == NULL) {
            fprintf(stderr, "Memory allocation failed\n");
            exit(1);
        }
    }

    // Deallocate memory
    for (i = 0; i < num_objects; i++) {
        free(objects[i]);
    }
    free(objects);
}

int main(int argc, char *argv[]) {
    clock_t start_time, end_time;
    double execution_time;

    // Check if the number of command-line arguments is correct
    if (argc != 2) {
        printf("Usage: %s <num_objects>\n", argv[0]);
        return 1;
    }

    int num_objects = atoi(argv[1]); // Convert the argument to an integer
    if (num_objects <= 0) {
        printf("Please enter a valid number of objects\n");
        return 1;
    }

    start_time = clock();
    simulate_memory_ops(num_objects); // Simulating operations on num_objects objects
    end_time = clock();

    execution_time = ((double)(end_time - start_time)) / CLOCKS_PER_SEC;

    // Print execution time and number of objects
    printf("Number of objects: %d\n", num_objects);
    printf("Execution time: %f seconds\n", execution_time);

    return 0;
}
