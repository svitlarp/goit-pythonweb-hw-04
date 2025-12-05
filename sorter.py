import argparse
import shutil
import logging
import asyncio
from pathlib import Path

# Logging program
logging.basicConfig(
    format='%(asctime)s, %(message)s',
    level=logging.WARNING,
        handlers=[
            logging.FileHandler('program log'),
            logging.StreamHandler()
        ]
)

def parse_args():
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', required=True, type=str, help='Source folder')
    parser.add_argument('-o', '--output', required=True, type=str, help='Output folder')
    return parser.parse_args()    

async def read_folder(source:Path, output:Path):
    """Recursively reads all files in a directory and its subdirectories."""
    tasks = []
    for f in source.iterdir():
        if f.is_dir():
            tasks.append(read_folder(f, output))
        else:
            tasks.append(copy_file(f, output))
    await asyncio.gather(*tasks)

async def copy_file(file:Path, output:Path):
    """Copies a file into a subforlder based on its extension"""
    try:
        ext = file.suffix.lstrip(".").lower()
        dest_dir = output / ext
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True)

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, shutil.copy2, file, dest_dir)
    except Exception as e:
        logging.error(f"Error copying {file}: {e}")

                 
async def main():
    args = parse_args()
    source = Path(args.source).resolve()
    output = Path(args.output).resolve()

    if not source.exists():
        print("source dir does not exist")
        return
    
    await read_folder(source, output)


if __name__ == "__main__":
    asyncio.run(main())

