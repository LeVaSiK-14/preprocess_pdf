import time
import functools

def measure_time(func):
    """
        Функция для замера скорости работы других.
        Используется в качестве декоратора.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start_time
        minutes = int(elapsed // 60)
        seconds = elapsed % 60
        print(f"Функция {func.__name__} выполнилась за {minutes} мин и {seconds:.2f} сек")
        return result
    return wrapper
