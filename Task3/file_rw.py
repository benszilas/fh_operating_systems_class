import datetime
import time

LENGTH = 25

def actual_timestamp():
    return datetime.datetime.now()

def write_to_file(filename: str):
    file1 = open(filename, "w")
    for i in range(LENGTH):
        print(f"Write Line: {i} {actual_timestamp()}")
        print(f"Write Line: {i} {actual_timestamp()}", file=file1)
        time.sleep(1)

def append_to_file(filename: str):
    file2 = open(filename, "a")
    for i in range(LENGTH):
        print(f"Append Line: {i} {actual_timestamp()}")
        print(f"Append Line: {i} {actual_timestamp()}", file=file2)
        time.sleep(1)

def read_from_file(filename: str):
    with open(filename) as file:
        for line in file:
            print(line, end='')
            time.sleep(1)

def main():
    write_to_file("file1.txt")
    append_to_file("file2.txt")
    read_from_file("file1.txt")
    read_from_file("file2.txt")

if __name__ == "__main__":
    main()
