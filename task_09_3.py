## Ассинхронный
import aiohttp
import aiofiles
import asyncio
import os
import sys
import time


async def download_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                filename = url.split('/')[-1]
                path = os.path.join('images_asynchronous', filename)
                os.makedirs('images_asynchronous', exist_ok=True)
                async with aiofiles.open(path, 'wb') as file:
                    await file.write(await response.read())
                print(f"Downloaded {filename}")
            else:
                print(f"Failed to download {url}")


async def async_downloader(urls):
    start_time = time.time()
    tasks = [download_image(url) for url in urls]
    await asyncio.gather(*tasks)
    end_time = time.time()
    print(f"Total execution time: {end_time - start_time} seconds")


if __name__ == "__main__":
    urls = sys.argv[1:]
    if not urls:
        print("Usage: python program.py <url1> <url2> ...")
        sys.exit(1)

    asyncio.run(async_downloader(urls))
