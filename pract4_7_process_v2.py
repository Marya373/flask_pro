"""
#### Задание #7
- Напишите программу на Python, которая будет находить
сумму элементов массива из 1000000 целых чисел.
- Пример массива: arr = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, ...]
- Массив должен быть заполнен случайными целыми числами
от 1 до 100.
- При решении задачи нужно использовать многопоточность,
многопроцессорность и асинхронность.
- В каждом решении нужно вывести время выполнения
вычислений.
"""
import time
import random
from multiprocessing import cpu_count, \
                            Process, \
                            Value


def generating_array() -> list[int]:

    array: list[int] = []

    for _ in range(1_000_000):
        array.append(random.randint(1, 100))

    return array


def split_array(array: list[int],
                num_parts: int) -> list[list[int]]:

    length = len(array)
    part_size = length // num_parts
    remainder = length % num_parts

    parts = []
    start = 0

    for i in range(num_parts):
        end = start + part_size
        if i < remainder:
            end += 1
        parts.append(array[start:end])
        start = end

    return parts


def sum_array(array: list[int], shared_value: Value) -> None:
    with shared_value.get_lock():
        shared_value.value += sum(array)


def main() -> None:

    shared_value = Value('i', 0)

    processes: list = []

    num_parts = cpu_count()

    array: list = generating_array()

    all_parts_array = \
        split_array(array=array, num_parts=num_parts)

    for part_array in all_parts_array:

        process = Process(target=sum_array, args=(part_array, shared_value))
        processes.append(process)
        # process.start()

    beginning_calculations = time.time()

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    end_calculations = time.time()

    print(f"Результат {shared_value.value}, "
          f"время вычисления: {end_calculations - beginning_calculations:.10f} секунд, "
          f"количество частей на которые разбита задача: {num_parts};")


if __name__ == '__main__':
    main()
