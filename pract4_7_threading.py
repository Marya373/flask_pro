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
import queue
import random
import threading


#result_queue = queue.Queue()


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


def sum_array(array: list[int], result_queue: queue.Queue) -> None:
#def sum_array(array: list[int]) -> None:
    result_queue.put(sum(array))


def main(num_parts: int = 1) -> None:

    threads: list = []

    result_queue = queue.Queue()

    array: list = generating_array()

    all_parts_array = \
        split_array(array=array, num_parts=num_parts)

    for part_array in all_parts_array:

        thread = threading.Thread(target=sum_array, args=[part_array, result_queue])
        threads.append(thread)
        #thread.start()

    beginning_calculations = time.time()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end_calculations = time.time()

    final_result: int = 0

    for _ in range(result_queue.qsize()):
        final_result += result_queue.get()

    print(f"Результат {final_result}, "
          f"время вычисления: {end_calculations - beginning_calculations:.10f} секунд, "
          f"количество частей на которые разбита задача: {num_parts};")


if __name__ == '__main__':
    main(num_parts=2)
