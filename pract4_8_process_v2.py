"""
#### Задание #8
- Напишите программу, которая будет скачивать страницы из
списка URL-адресов и сохранять их в отдельные файлы на
диске.
- В списке может быть несколько сотен URL-адресов.
- При решении задачи нужно использовать многопоточность,
многопроцессорность и асинхронность.
- Представьте три варианта решения.
"""
import math
import time
import requests
from pathlib import Path
from multiprocessing import Lock, Process, cpu_count


START_PROGRAM_TIME = time.time()


def download(url: str, lock: Lock):

    response = requests.get(url)

    filename = 'pract4_8_process_v2.txt'

    file = Path().cwd() / filename

    with lock:

        with open(file, "a", encoding='utf-8') as file:
            file.write('\n\n' + url + '\n\n')
            file.write(response.text)

        print(f"URL: {url} скачано за {time.time() - START_PROGRAM_TIME:.6f} секунд.")


def split_array(array: list[str],
                num_parts: int) -> list[list[str]]:

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


def main(urls: list) -> None:

    lock = Lock()

    num_parts: int = \
        math.ceil(len(urls) / cpu_count())

    split_urls = \
        split_array(num_parts=num_parts,
                    array=urls)

    for part_urls in split_urls:

        processes: list = []

        for url in part_urls:
            process = Process(target=download, args=(url, lock))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()


if __name__ == '__main__':

    urls = \
        [
            'https://www.google.ru/',
            'https://ya.ru/',
            'https://www.python.org/',
            'https://habr.com/ru/all/',
            'https://hh.ru/'
        ]

    main(urls=urls)
