import logging
import time
from functools import wraps

logging.basicConfig(
    filename="logs/server.log",  # all logs go into this file
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
def log_execution(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start=time.time()
        result=func(*args,**kwargs)
        end=time.time()
        function_runtime=end-start
        if(function_runtime>1):
            logging.warning(f"{func.__name__} took {function_runtime:.2f} seconds")
        else:
            logging.info(f"{func.__name__} took {function_runtime:.2f} seconds")
        
        return result
    
    return wrapper

@log_execution
def slow_function():
    time.sleep(2)
    print("function exceuted")

from collections import deque



if __name__ == "__main__":
    slow_function()