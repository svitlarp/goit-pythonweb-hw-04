import argparse
import shutil
import logging
from pathlib import Path


logging.basicConfig(
    format='%(asctime)s, %(message)s',
    level=logging.WARNING,
        handlers=[
            logging.FileHandler('program log'),
            logging.StreamHandler()
        ]
)

def parse_args():
    """Function that parse arguments from cli"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--source', required=True, type=str, help='Source folder')
    parser.add_argument('-o', '--output', required=True, type=str, help='Output folder')
    return parser.parse_args()    

def read_folder(source:Path, output:Path):
    for f in source.iterdir():
        if f.is_dir():
            read_folder(f, output)
        else:
            copy_file(f, output)

def copy_file(file:Path, output:Path):
    try:
        ext = file.suffix.lstrip(".").lower()
        dest_dir = output / ext
        if not dest_dir.exists():
            dest_dir.mkdir(parents=True)

        shutil.copy(file, dest_dir)
    except Exception as e:
        logging.error(f"Error copying {file}: {e}")

                 
def main():
    args = parse_args()
    source = Path(args.source).resolve()
    output = Path(args.output).resolve()

    if not source.exists():
        print("source dir does not exist")
        return
    
    read_folder(source, output)


if __name__ == "__main__":
    main()

