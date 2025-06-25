import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from app.main.FileNames import saveFile, discardFile

class AsyncFileCounter:
    def __init__(self, directory, extensions):
        self.directory = directory
        self.extensions = list(map(lambda e:e.lower(), extensions))
        self.executor = ThreadPoolExecutor()

    def _count_files_sync(self):
        total = 0
        completed = 0
        savePath = self.directory + "\\" + saveFile
        discardPath = self.directory + "\\" + discardFile
        for root, _, files in os.walk(self.directory):
            for file in files:
                location = file.rfind('.')
                if file[location:] in self.extensions:
                    if root == savePath or root == discardPath:
                        completed += 1
                    total += 1
        return completed, total

    async def count_files(self):
        loop = asyncio.get_running_loop()
        completed, total = await loop.run_in_executor(self.executor, self._count_files_sync)
        return completed, total

# Example usage:
# async def main():
#     counter = AsyncFileCounter("/path/to/your/folder", ".jpg")
#     count = await counter.count_files()
#     print(f"Found {count} files.")

# asyncio.run(main())