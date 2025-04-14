import time
import functools
import logging
from requests.exceptions import RequestException

logging.basicConfig(level=logging.INFO)

def retry_on_exception(
    exceptions=(RequestException,),
    max_retries=3,
    initial_delay=1,
    backoff_factor=2,
    max_delay=30
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay
            while True:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    retries += 1
                    if retries > max_retries:
                        logging.error(f"Max retries exceeded: {e}")
                        return
                    logging.info(f"Retrying ({retries}/{max_retries}) in {delay}s due to: {e}")
                    time.sleep(min(delay, max_delay))
                    delay *= backoff_factor
        return wrapper
    return decorator

if __name__=="__main__":
    import requests
    
    @retry_on_exception()
    def send_request(*args, **kwargs):
        return requests.request(*args, **kwargs)
    
    r = send_request('GET', 'https://httpbin.org/ip', timeout=3)
    if r.ok:
        print(r.json())