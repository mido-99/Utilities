import time
import functools
from requests.exceptions import RequestException
import logging


def retry_on_exception(
    exceptions=(RequestException,),
    max_retries=3,
    initial_delay=1,
    backoff_factor=2,
    max_delay=30,
    on_retry=None,
    on_success=None,
    on_failure=None,
    logger=logging,
):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay
            
            while True:
                try:
                    result = func(*args, **kwargs)
                    if on_success:
                        on_success(result)
                    return result
                
                except exceptions as e:
                    retries += 1
                    if retries > max_retries:
                        logging.error(f"Max retries exceeded: {e}")
                        if on_failure:
                            on_failure(e)
                        return
                    
                    logging.warning(f"Retrying ({retries}/{max_retries}) in {delay}s due to: {e}")
                    if on_retry:
                        on_retry(e)
                    time.sleep(min(delay, max_delay))
                    delay *= backoff_factor
        return wrapper
    return decorator

if __name__=="__main__":
    import requests
    from requests import Response
    
    logging.basicConfig(level=logging.INFO)
    
    def on_retry(e):
        logging.info(f"Retrying due to: {e}")
    def on_success(r: Response):
        logging.info("Request succeeded")
        if r.ok:
            logging.info(r.json())
    def on_failure(e):
        logging.info(f"Request failed: {e}")
    
    @retry_on_exception(on_retry=on_retry, on_success=on_success, on_failure=on_failure)
    def send_request(*args, **kwargs):
        return requests.request(*args, **kwargs)
    
    r = send_request('GET', 'https://httpbin.org/ip', timeout=5)