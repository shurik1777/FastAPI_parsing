## Многопроцессорный
import requests
import os
import time
import multiprocessing
import sys


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        filename = url.split('/')[-1]
        path = os.path.join('images_proces', filename)
        os.makedirs('images_proces', exist_ok=True)
        with open(path, 'wb') as file:
            file.write(response.content)
        print(f"Downloaded {filename}")
    else:
        print(f"Failed to download {url}")


def multi_process_downloader(urls):
    start_time = time.time()
    processes = []
    for url in urls:
        process = multiprocessing.Process(target=download_image, args=(url,))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    end_time = time.time()
    print(f"Total execution time: {end_time - start_time} seconds")


if __name__ == "__main__":
    urls = sys.argv[1:]
    if not urls:
        print("Usage: python program.py <url1> <url2> ...")
        sys.exit(1)

    multi_process_downloader(urls)
