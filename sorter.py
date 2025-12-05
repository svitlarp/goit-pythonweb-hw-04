import argparse
import shutil
from pathlib import Path


def parse_args():
    """Function that parse arguments from cli"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filename', type=str, help='Filename')
    args = parser.parse_args()

    if args.filename:
        print(f"filename from cli: {args.filename}")
        return args.filename
    

def apply_file_type_method(path):
    if path.is_dir():
        handleDir(path)
    else:
        handleFile(path)
        

def handleDir(dir: Path):
    for file in dir.iterdir():
        if file.is_file():
            handleFile(file)

                 
def handleFile(file: Path):
    ext = file.suffix.lstrip(".")
    source_dir = file.parent
    target_dir = source_dir / ext
    if target_dir.exists():
        # Move file to the directory
        shutil.move(file, target_dir)
    else:
        # Create the directory
        target_dir.mkdir()

        # Move file to the directory
        shutil.move(file, target_dir)

def main():
    filename = parse_args()
    apply_file_type_method(Path(filename))


if __name__ == "__main__":
    main()

