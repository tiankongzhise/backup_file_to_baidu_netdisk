import time
from contextlib import contextmanager

@contextmanager
def breanch_time(msg:str):
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        print(f"{msg} time: {end_time - start_time:.2f} seconds")