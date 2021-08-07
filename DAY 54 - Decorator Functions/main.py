import time

def speed_calc_decorator(function):
    def wrapper_function():
        start_time = time.time()
        function()
        end_time = time.time()

        if function.__name__ == 'fast_function':
            print(f"The time it takes to run fast function: {end_time - start_time:.2f}")
        elif function.__name__ == 'slow_function':
            print(f"The time it takes to run slow function: {end_time - start_time:.2f}")
        
    return wrapper_function

@speed_calc_decorator
def fast_function():
    for i in range(10000000):
        i * i

@speed_calc_decorator
def slow_function():
    for i in range(100000000):
        i * i

fast_function()
slow_function()