"""
#### Задание #9
- Написать программу, которая скачивает изображения с заданных URL-адресов и
сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
файле, название которого соответствует названию изображения в URL-адресе.
- Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
image1.jpg
- Программа должна использовать многопоточный, многопроцессорный и
асинхронный подходы.
- Программа должна иметь возможность задавать список URL-адресов через
аргументы командной строки.
- Программа должна выводить в консоль информацию о времени скачивания
каждого изображения и общем времени выполнения программы.
"""
import math
import time
import requests
from sys import argv
from pathlib import Path
from multiprocessing import Process, cpu_count


def download(url: str, start_work: time.time):

    response = requests.get(url)

    directory_for_save = 'pract4_9_process_v2'

    directory_for_save = Path().cwd() / directory_for_save

    if not Path(directory_for_save).exists():
        Path(directory_for_save).mkdir()

    url_list = url.split('/')

    filename = url_list[len(url_list)-1]

    file = directory_for_save / filename

    with open(file, "wb") as file:

        file.write(response.content)

        print(f"URL: {url} скачано за {time.time() - start_work:.6f} секунд.")


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

    start_work = time.time()

    num_parts: int = \
        math.ceil(len(urls) / cpu_count())

    split_urls = \
        split_array(num_parts=num_parts,
                    array=urls)

    for part_urls in split_urls:

        processes: list = []

        for url in part_urls:
            process = Process(target=download, args=(url, start_work))
            processes.append(process)
            process.start()

        for process in processes:
            process.join()

    print(f"Суммарное время скачивания {time.time() - start_work:.6f} секунд.")


if __name__ == "__main__":

    if len(argv) >= 2:

        urls: list = []

        for url in argv[1:]:
            urls.append(url)

        main(urls=urls)

    else:
        print("Введено неверное количество аргументов")



