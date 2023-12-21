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
import asyncio


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


async def sum_array(array: list[int]):
    return sum(array)


async def main(num_parts: int = 1) -> None:

    tasks: list = []

    array: list = generating_array()

    all_parts_array = \
        split_array(array=array, num_parts=num_parts)

    for part_array in all_parts_array:

        #task = asyncio.ensure_future(character_counter_in_file(file))
        task = asyncio.create_task(sum_array(array=part_array))
        tasks.append(task)

    beginning_calculations = time.time()

    await asyncio.gather(*tasks)

    end_calculations = time.time()

    final_result: int = 0

    for task in tasks:
        final_result += task.result()

    print(f"Результат {final_result}, "
          f"время вычисления: {end_calculations - beginning_calculations:.10f} секунд, "
          f"количество частей на которые разбита задача: {num_parts};")


if __name__ == '__main__':
    asyncio.run(main(num_parts=1))
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main(num_parts=1))
