"""
#### Задание #3
- Написать программу, которая считывает список из 10 URL-
адресов и одновременно загружает данные с каждого адреса.
- После загрузки данных нужно записать их в отдельные
файлы.
- Используйте асинхронный подход.
"""
import time
import asyncio
import aiohttp
from pathlib import Path


urls = \
    [
        'https://www.google.ru/',
        'https://gb.ru/',
        'https://ya.ru/',
        'https://www.python.org/',
        'https://habr.com/ru/all/',
        'https://mail.ru/',
        'https://github.com/',
        'https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0',
        'https://news.vtomske.ru/',
        'https://www.1tv.ru/'
     ]


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()
            directory_for_save = 'practica_4_task_3'
            filename = 'asyncio_' + url.replace('https://','').replace('.', '_').replace('/', '') + '.html'

            current_file = Path(__file__)
            parent_directory = current_file.parent
            directory_for_save = parent_directory / directory_for_save

            if not Path(directory_for_save).exists():
                Path(directory_for_save).mkdir()

            filename = directory_for_save / filename

            with open(filename, "w", encoding='utf-8') as f:
                f.write(text)
                print(f"Downloaded {url} in {time.time() -start_time:.2f} seconds")


async def main():
    tasks = []

    for url in urls:
        #task = asyncio.ensure_future(download(url))
        task = asyncio.create_task(download(url))
        tasks.append(task)

    await asyncio.gather(*tasks)

start_time = time.time()

if __name__ == '__main__':
    asyncio.run(main())
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
