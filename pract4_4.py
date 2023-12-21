"""
#### Задание #4
- Создать программу, которая будет производить подсчет
количества слов в каждом файле в указанной директории и
выводить результаты в консоль.
- Используйте потоки.
"""
import time
import threading
from pathlib import Path


START_PROGRAM_TIME = time.time()


def character_counter_in_file(filename: Path | str):

    with open(filename, "r", encoding='utf-8') as file:

        content = file.read()

        character_counter = len(content.split(' '))

    filename = filename.name

    print(f"Файл {filename} содержит {character_counter} символов"
          f" рассчитано за {time.time() - START_PROGRAM_TIME:.6f} секунд.")


def main(set_dir: str | Path) -> None:

    threads = []

    directory = Path().cwd() / set_dir

    for file in directory.iterdir():

        if file.is_file():

            thread = threading.Thread(target=character_counter_in_file, args=[file])
            threads.append(thread)
            #thread.start()

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main(set_dir='pract_4_1')