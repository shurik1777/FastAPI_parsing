"""
Задание №9.
� Написать программу, которая скачивает изображения с заданных URL-адресов и
сохраняет их на диск. Каждое изображение должно сохраняться в отдельном
файле, название которого соответствует названию изображения в URL-адресе.
� Например URL-адрес: https://example/images/image1.jpg -> файл на диске:
image1.jpg
� Программа должна использовать многопоточный, многопроцессорный и
асинхронный подходы.
� Программа должна иметь возможность задавать список URL-адресов через
аргументы командной строки.
� Программа должна выводить в консоль информацию о времени скачивания
каждого изображения и общем времени выполнения программы.
"""
## Многопоточный

import requests
import os
import time
import threading
import sys


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split('/')[-1]
        path = os.path.join('images_multi_threaded', filename)
        os.makedirs('images_multi_threaded', exist_ok=True)
        with open(path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {url}")


def multi_threaded_downloader(urls):
    start_time = time.time()
    threads = []
    for url in urls:
        thread = threading.Thread(target=download_image, args=(url,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time} seconds")


if __name__ == "__main__":
    urls = sys.argv[1:]
    if not urls:
        print("Usage: python program.py <url1> <url2> ...")
        sys.exit(1)

    multi_threaded_downloader(urls)
