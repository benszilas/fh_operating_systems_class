import sys, time

if (len(sys.argv) > 1):
    some_str = ' ' * 1024 * 1024 * 1024 * int(sys.argv[1])

while 1:
    print("true")
    time.sleep(1)
