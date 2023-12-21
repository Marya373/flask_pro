"""
#### Задание #6
- Создать программу, которая будет производить подсчет
количества слов в каждом файле в указанной директории и
выводить результаты в консоль.
- Используйте асинхронный подход.
"""
import time
import asyncio
import aiofiles
from pathlib import Path


START_PROGRAM_TIME = time.time()


async def character_counter_in_file(filename: Path | str):

    async with aiofiles.open(filename, "r", encoding='utf-8') as file:

        content = await file.read()

        character_counter = len(content.split(' '))

    filename = filename.name

    print(f"Файл {filename} содержит {character_counter} символов"
          f" рассчитано за {time.time() - START_PROGRAM_TIME:.6f} секунд.")


async def main(set_dir: str | Path) -> None:

    tasks = []

    directory = Path().cwd() / set_dir

    for file in directory.iterdir():

        if file.is_file():
            #task = asyncio.ensure_future(character_counter_in_file(file))
            task = asyncio.create_task(coro=character_counter_in_file(file))
            tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main(set_dir='pract4_1'))
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
