import functools
import time
import queue


def time_mean_last_k_calls(k: int):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            wrapper.call_times.append(end - start)
            
            average_time = sum(wrapper.call_times) / len(wrapper.call_times)
            print(f"Среднее время выполнения последних k = {len(wrapper.call_times)} вызовов: {average_time:.2f} сек.")
            if len(wrapper.call_times) >= k:
                wrapper.call_times.pop(0)
            return result
        wrapper.call_times = []
        return wrapper
    return decorator


@time_mean_last_k_calls(10)
def foo(arg1):
    time.sleep(0.5)

for _ in range(12):
    foo("Walter")













