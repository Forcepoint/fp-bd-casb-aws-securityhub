import os


def create_file(f, f_content):
    with open(f, "w") as fil:
        fil.write(f_content)


def delete_file_content(f):
    open(f, "w").close()


def delete_files(f_lst):
    for f in f_lst:
        os.remove(f)
