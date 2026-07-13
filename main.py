import os
from datetime import datetime, timedelta 
import argparse

parser = argparse.ArgumentParser(description="Directory file manage")

parser.add_argument("--dir", type=str, help="the directory to scan")

args = parser.parse_args()

def last_access_time(info):
    """get the last access time"""
    last_access_time = datetime.fromtimestamp(info.st_atime)
    
    return last_access_time


def last_mod_time(info):
    """get the last modified date"""
    last_mod_time = datetime.fromtimestamp(info.st_mtime)
    
    return last_mod_time


def get_never_used_files(path):
    """Return a list of never opened files"""
    list = []
    try:
        for entry in os.scandir(path):
            try:
                is_dir = entry.is_dir(follow_symlinks=False)
            except OSError as error:
                print('Error calling is_dir():', error, file=sys.stderr)
                continue
            if is_dir:
            
                list.append(entry.path)
                get_never_used_files(entry.path)
            else:
                try:
                    info = entry.stat(follow_symlinks=False)
                
                    if last_access_time(info) == last_mod_time(info):

                        list.append(entry.path)
                except OSError as error:
                    print('Error calling stat():', error, file=sys.stderr)
    except NotADirectoryError as error:
        print('The path is not a folder: ' + path)
    return list

path = args.dir or "."


 
print(*get_never_used_files(path), sep="\n")
