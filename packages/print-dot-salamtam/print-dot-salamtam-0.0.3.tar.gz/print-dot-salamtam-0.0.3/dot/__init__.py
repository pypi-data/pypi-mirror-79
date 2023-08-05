import time


class Dot:
    def print_one(self):
        print(".")

    def print_two(self):
        print("..")

    def print_every_1_sec(self):
        while True:
            print(".")
            time.sleep(1)
