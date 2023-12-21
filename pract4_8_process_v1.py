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
import time
import requests
from pathlib import Path
from multiprocessing import Lock, Process


START_PROGRAM_TIME = time.time()


def download(url: str, lock: Lock):

    response = requests.get(url)

    filename = 'pract4_8_process_v1.txt'

    file = Path().cwd() / filename

    with lock:

        with open(file, "a", encoding='utf-8') as file:
            file.write('\n\n' + url + '\n\n')
            file.write(response.text)

            print(f"URL: {url} скачано за {time.time() - START_PROGRAM_TIME:.6f} секунд.")


def main(urls: list) -> None:

    lock = Lock()

    processes: list = []

    for url in urls:
        process = Process(target=download, args=(url, lock))
        processes.append(process)
        #processes.start()

    for process in processes:
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
