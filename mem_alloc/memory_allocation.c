#include <stdio.h>
#include <stdlib.h>

// Function to allocate memory for objects
void allocate_objects(int num_objects) {
    // Assuming each object is of size int (4 bytes)
    int *objects = (int *)malloc(num_objects * sizeof(int));
    if (objects == NULL) {
        printf("Memory allocation failed.\n");
        exit(1);
    }
    printf("Memory allocated for %d objects.\n", num_objects);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <num_objects>\n", argv[0]);
        return 1;
    }

    int num_objects = atoi(argv[1]);
    allocate_objects(num_objects);

    // To print memory usage, you may use system-specific functions
    // Here, we just print the size of allocated memory in bytes
    size_t memory_usage = num_objects * sizeof(int);
    printf("Memory usage: %zu bytes\n", memory_usage);

    // Simulating deallocation
    // free(objects); // Uncomment if you want to deallocate memory

    return 0;
}
