from pathlib import Path
import requests
import time
import argparse
import threading
from multiprocessing import Process
import asyncio
import aiohttp

# Объявляем пустой список для хранения ссылок на изображения
images = []
# Открываем файл прямыми ссылками на изображения, читаем его и добавляем каждую строку в список images
with open('images.txt', 'r') as f:
    for image in f.readlines():
        images.append(image.strip())
# Создаем объект Path для пути к директории, директории, куда будут сохраняться изображения
PATH = Path('images')


# Определяем функцию для загрузки изображения с использованием библиотеки requests
def download_img(url, dir_path=PATH):
    start_time = time.time()  # Запоминаем время начала загрузки
    response = requests.get(url)  # Получаем ответ от сервера
    filename = url.split('/')[-1]  # Получаем имя файла из URL
    with open(dir_path / filename, 'wb') as f:  # Открываем файл для записи
        for data in response.iter_content(1024):  # Читаем данные блоками по 1024 байт
            f.write(data)  # Записываем данные в файл
    end_time = time.time() - start_time  # Вычисляем время загрузки
    print(f'Загрузка {filename} заняла {end_time:.2f} сек')  # Выводим время загрузки


# Определяем функцию для парсинга аргументов командной строки
def parse():
    parser = argparse.ArgumentParser(description='Парсер изображений по URL-адресам')
    parser.add_argument('-u', '--urls', default=images, nargs='+', type=str, help='Список URL-адресов')
    return parser.parse_args()


# Определяем асинхронную версию функции загрузки изображения с использованием aiohttp
async def download_img_as(url, dir_path=PATH):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:  # Используем асинхронный сеанс HTTP
        async with session.get(url) as response:  # Получаем ответ от сервера асинхронно
            item = await response.read()  # Читаем тело ответа асинхронно
            filename = url.split('/')[-1]  # Получаем имя файла из URL
            with open(dir_path / filename, 'wb') as f:
                f.write(item)
    end_time = time.time() - start_time
    print(f'Загрузка {filename} заняла {end_time:.2f} сек')


# Определяем функцию для загрузки изображений с использованием потоков
def download_img_thread(urls):
    threads = []  # Список для хранения объектов потоков
    start_time = time.time()  # Запоминаем время начала загрузки

    for url in urls:
        thread = threading.Thread(target=download_img, args=(url,))  # Создаем поток
        threads.append(thread)  # Добавляем поток в список
        thread.start()  # Запускаем поток

    for thread in threads:
        thread.join()  # Ожидаем завершения всех потоков

    end_time = time.time() - start_time  # Вычисляем общее время загрузки
    print(f'Загрузка заняла {end_time:.2f} сек')


# Определяем функцию для загрузки изображений с использованием процессов
def download_img_process(urls):
    processes = []  # Список для хранения объектов процессов
    start_time = time.time()  # Запоминаем время начала загрузки

    for url in urls:
        process = Process(target=download_img, args=(url,))
        processes.append(process)  # Добавляем процесс, процесс в список
        process.start()  # Запускаем процесс

    for process in processes:
        process.join()  # Ожидаем завершения всех процессов

    end_time = time.time() - start_time
    print(f'Загрузка заняла {end_time:.2f} сек')


# Определяем асинхронную функцию для загрузки изображений с использованием asyncio
async def download_img_async(urls):
    tasks = []
    start_time = time.time()

    for url in urls:  # перебираются все URL-адреса изображений
        task = asyncio.create_task(download_img_as(url))  # создаётся новая асинхронная задача
        tasks.append(task)

    await asyncio.gather(*tasks)  # После создания всех асинхронных задач, они собираются

    end_time = time.time() - start_time
    print(f'Загрузка заняла {end_time:.2f} сек')


# Если текущий скрипт запущен как основной, выполняем остальную часть кода
if __name__ == '__main__':
    urls = parse().urls  # Парсим аргументы командной строки

    if not PATH.exists():  # Проверяем существование директории для сохранения изображений
        PATH.mkdir()

    print(f'Загрузка {len(urls)} изображений через мультипотоки')
    download_img_thread(urls)

    print(f'Загрузка {len(urls)} изображений через мультипроцессы')
    download_img_process(urls)

    print(f'Загрузка {len(urls)} изображений асинхронно')
    asyncio.run(download_img_async(urls))  # Запускаем асинхронную функцию
