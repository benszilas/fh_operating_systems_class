import subprocess
import threading
import io
import os
import stat
from pathlib import Path

semaphore = threading.Semaphore(2)


def is_prime(n: int) -> bool:
    """
    tests if a number is prime

    :param n: the integer to test
    :type n: int
    :return: true if prime
    :rtype: bool
    """
    # base cases 0-3
    if n <= 1:
        return False
    if n <= 3:
        return True

    # 6k + i primality test algorithm
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6
    return True


def create_output_file(input_filename: Path) -> io.TextIOWrapper:
    """
    creates an output file as required in the task

    target directory is the input file directory

    Example: 1-10000.csv -> 2-20000.csv

    :param input_filename: absolute path of input file
    :type input_filename: Path
    """
    try:
        # double the input file name range
        parent_dir = input_filename.parent
        numbers = [int(number) for number in input_filename.stem.split("-")]
        if len(numbers) != 2:
            raise RuntimeError(f"invalid input file name {input_filename}")

        # range is the input file range * 2
        output_file_range = str(numbers[0] * 2) + "-" + str(numbers[1] * 2)
        output_filename = Path(parent_dir, output_file_range + ".csv")

        # open for writing, and set permission 600 using stat and bitwise or
        output_file = open(output_filename, mode="w", encoding="UTF-8")
        os.chmod(output_filename, stat.S_IWUSR | stat.S_IRUSR)
    except Exception as e:
        raise RuntimeError(
            f"error creating output file: {e} in thread {threading.current_thread()}"
        ) from e
    return output_file


def thread_routine(filename: Path):
    """
    do the task for one file

    :param filename: input file absolute path
    :type filename: Path
    """
    filepath = Path(__file__).resolve().parent
    try:
        with open(filename, encoding="UTF-8") as input_file:
            output_file = create_output_file(filename)
            output_list: list[int] = []
            for line in input_file:
                input_number = None
                try:
                    input_number = int(line)
                except ValueError as e:
                    # catch value error per line, just in case the input file is malformated somehow
                    # input_number for this line will stay None
                    # to skip the primality test and calc.sh script
                    # continue parsing the rest of the file
                    print(f"error reading {line=} from {filename=}: {e}")

                # no try-except here ->
                # if an error happens in the subprocess, print it and stop parsing the file
                # capture output to read from the stdout of calc.sh script
                if input_number is not None and is_prime(input_number):
                    # aquire semaphore to make sure no more than 2 threads run the calc.sh script
                    # use context management to release the semaphore if an exception occurs
                    with semaphore:
                        process = subprocess.run(
                            args=[Path(filepath, "calc.sh"), str(input_number)],
                            capture_output=True,
                            check=True,
                        )
                    result = int(process.stdout)
                    if is_prime(result):
                        output_list.append(result)

            # sort the output and print it to the output file
            output_list.sort()
            for number in output_list:
                print(number, file=output_file)

    except Exception as e:
        print(f"error in thread {threading.current_thread().name}: {e}")


def main():
    """
    declare .csv input files

    spawn and join threads
    """
    # create Path objects with the file names
    filepath = Path(__file__).resolve().parent
    files = [
        Path(filepath, "1-10000.csv"),
        Path(filepath, "10001-20000.csv"),
        Path(filepath, "20001-30000.csv"),
        Path(filepath, "30001-40000.csv"),
        Path(filepath, "40001-50000.csv"),
        Path(filepath, "50001-60000.csv"),
    ]
    threads = []

    for i in range(len(files)):
        try:
            spawned_thread = threading.Thread(target=thread_routine, args=(files[i],))
            threads.append(spawned_thread)
            spawned_thread.start()
        except Exception as e:
            print(f"error spawning thread {i}: {e}")

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()
