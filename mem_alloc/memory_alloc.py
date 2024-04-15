import subprocess
import psutil
import matplotlib.pyplot as plt

def allocate_objects_python(num_objects):
    objects = []
    for _ in range(num_objects):
        objects.append(object())
    return objects

def simulate_memory_allocation_python(num_objects, num_trials):
    python_memory_usage = []

    for _ in range(num_trials):
        objects_python = allocate_objects_python(num_objects)
        python_memory_usage.append(psutil.Process().memory_info().rss)
        del objects_python

    return python_memory_usage

def simulate_memory_allocation_c(num_objects, num_trials):
    c_memory_usage = []

    for _ in range(num_trials):
        # Execute the compiled C program and capture its output
        output = subprocess.check_output(["C:\\Users\\medav\\Documents\\GitHub\\garbagec_non_debate\\mem_alloc\\memory_allocation_c.exe", str(num_objects)]).decode().split("\n")
        for line in output:
            if "Memory usage" in line:
                memory_usage_str = line.split(":")[1].strip()
                memory_usage = int(memory_usage_str.split()[0])  # Extract numeric part
                c_memory_usage.append(memory_usage)

    return c_memory_usage


def plot_results(python_memory_usage, c_memory_usage):
    plt.plot(range(len(python_memory_usage)), python_memory_usage, label='Python Memory Usage')
    plt.plot(range(len(c_memory_usage)), c_memory_usage, label='C Memory Usage')
    plt.xlabel('Trial')
    plt.ylabel('Memory Usage (bytes)')
    plt.title('Memory Usage Comparison')
    plt.ylim(bottom=0)  # Set the bottom limit of the y-axis to 0
    plt.legend()
    plt.show()


def main():
    num_objects = 1000000  # Number of objects to allocate
    num_trials = 100  # Number of trials

    python_memory_usage = simulate_memory_allocation_python(num_objects, num_trials)
    c_memory_usage = simulate_memory_allocation_c(num_objects, num_trials)

    plot_results(python_memory_usage, c_memory_usage)

if __name__ == "__main__":
    main()
