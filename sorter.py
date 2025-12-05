import argparse
import shutil
import asyncio
import logging
from pathlib import Path


logging.basicConfig(
    format='%(asctime)s, %(message)s',
    level=logging.DEBUG,
        handlers=[
            logging.FileHandler('program log'),
            logging.StreamHandler()
        ]
)

def parse_args():
    """Function that parse arguments from cli"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, help='Filename')
    args = parser.parse_args()

    if args.filename:
        print(f"filename from cli: {args.filename}")
        return args.filename
    

async def apply_file_type_method(path):
    if path.is_dir():
        await handleDir(path)
    else:
        await handleFile(path)
        

async def handleDir(dir: Path):
    tasks = []
    for file in dir.iterdir():
        if file.is_file():
            tasks.append(handleFile(file))
    await asyncio.gather(*tasks)

                 
async def handleFile(file: Path):
    ext = file.suffix.lstrip(".")
    source_dir = file.parent
    target_dir = source_dir / ext

    loop = asyncio.get_event_loop()

    if not target_dir.exists():
        # Move file to the directory
        await loop.run_in_executor(None, target_dir.mkdir)

    # Move file to the directory
    await loop.run_in_executor(None, shutil.move, file, target_dir)

async def main():
    filename = parse_args()
    await apply_file_type_method(Path(filename))


if __name__ == "__main__":
    asyncio.run(main())

