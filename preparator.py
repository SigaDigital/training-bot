import os, shutil

def empty_directory(path):
    if  os.path.exists(path):
        shutil.rmtree(path)

    if not os.path.exists(path):
        os.makedirs(path)