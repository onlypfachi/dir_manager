import os
from datetime import datetime, timedelta 

current_dir = os.getcwd()
dir_files = os.listdir()

def last_access_time(info):
    """get the last access time"""
    last_access_time = datetime.fromtimestamp(info.st_atime)
    
    return last_access_time


def last_mod_time(info):
    """get the last modified date"""
    last_mod_time = datetime.fromtimestamp(info.st_mtime)
    
    return last_mod_time


def get_never_used_files(path):
    """Return a list of never opened files 
    """
    list = []
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
    return list

print(*get_never_used_files("."), sep="\n")
