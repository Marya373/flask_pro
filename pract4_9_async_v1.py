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
import time
import asyncio
import aiohttp
from sys import argv
from pathlib import Path


async def download(url: str, start_work: time.time):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            img = await response.read()

            directory_for_save = 'pract4_9_async_v1'

            directory_for_save = Path().cwd() / directory_for_save

            if not Path(directory_for_save).exists():
                Path(directory_for_save).mkdir()

            url_list = url.split('/')

            filename = url_list[len(url_list)-1]

            file = directory_for_save / filename

            with open(file, "wb") as file:

                file.write(img)

                print(f"URL: {url} скачано за {time.time() - start_work:.6f} секунд.")


async def main(urls: list) -> None:

    tasks: list = []

    start_work = time.time()

    for url in urls:
        #task = asyncio.ensure_future(download(url))
        task = asyncio.create_task(download(url=url,
                                            start_work=start_work))
        tasks.append(task)

    await asyncio.gather(*tasks)

    print(f"Суммарное время скачивания {time.time() - start_work:.6f} секунд.")


if __name__ == "__main__":

    if len(argv) >= 2:

        urls: list = []

        for url in argv[1:]:
            urls.append(url)

        asyncio.run(main(urls=urls))
        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(main(urls=urls))

    else:
        print("Введено неверное количество аргументов")



