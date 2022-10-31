import os
import time

if __name__ == "__main__":
    n = 100000
    for i in range(n):
        start_time = time.time()
        # python crawler.py x > {}\error_x.csv
        error_path = ""
        os.system(r"python crawler.py {} > {}\error_{}.csv".format(i, error_path, i))

        duration = time.time() - start_time
        print(f"Finish task {i} in {duration} seconds")

