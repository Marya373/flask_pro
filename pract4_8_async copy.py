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
import asyncio
import aiohttp
from pathlib import Path


START_PROGRAM_TIME = time.time()


urls = \
    [
        'https://www.google.ru/',
        'https://ya.ru/',
        'https://www.python.org/',
        'https://habr.com/ru/all/',
        'https://hh.ru/'
        
     ]


async def download(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            text = await response.text()

            filename = 'pract4_8_async.txt'

            file = Path().cwd() / filename

            with open(file, "a", encoding='utf-8') as file:

                file.write(text)

                print(f"URL: {url} скачано за {time.time() - START_PROGRAM_TIME:.6f} секунд.")


async def main():
    tasks = []

    for url in urls:
        #task = asyncio.ensure_future(download(url))
        task = asyncio.create_task(download(url))
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
