import time
import sys

# Function to simulate memory allocation and deallocation
def simulate_memory_ops(num_objects):
    objects = []
    # Allocate memory
    for _ in range(num_objects):
        objects.append([0] * 1000)  # Creating a list of 1000 integers

    # Deallocate memory
    del objects
    time.sleep(1)  # Simulating some processing time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <num_objects>")
        sys.exit(1)

    try:
        num_objects = int(sys.argv[1])
        if num_objects <= 0:
            raise ValueError
    except ValueError:
        print("Please enter a valid number of objects")
        sys.exit(1)

    start_time = time.time()
    simulate_memory_ops(num_objects)
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Number of objects: {num_objects}")
    print(f"Execution time: {execution_time} seconds")
