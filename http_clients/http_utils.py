import functools
import curl_cffi.requests
from curl_cffi.requests.exceptions import CurlError, RequestException
import logging
import asyncio


def retry_on_exception(
    exceptions=(Exception,),
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
        async def wrapper(*args, **kwargs):
            retries = 0
            delay = initial_delay
            
            while True:
                try:
                    result = await func(*args, **kwargs)
                    if on_success:
                        await on_success(result) if asyncio.iscoroutinefunction(on_success) else on_success(result)
                    return result
                
                except exceptions as e:
                    retries += 1
                    if retries > max_retries:
                        if on_failure:
                            await on_failure(e) if asyncio.iscoroutinefunction(on_failure) else on_failure(e)
                        else:
                            logging.error(f"Max retries exceeded: {e}")
                        return
                    
                    if on_retry:
                        await on_retry(e, retries=retries, max_retries=max_retries) if asyncio.iscoroutinefunction(on_retry) \
                        else on_retry(e, retries=retries, max_retries=max_retries)
                    else:
                        logging.warning(f"Retrying ({retries}/{max_retries}) in {delay}s due to: {e}")
                    await asyncio.sleep(min(delay, max_delay))
                    delay *= backoff_factor
        return wrapper
    return decorator

if __name__=="__main__":
    import curl_cffi
        
    logging.basicConfig(level=logging.INFO)
        
    async def on_retry(*args, **kwargs):
        e = args[0]
        if isinstance(e, (CurlError, RequestException)):
            logging.warning(f"Connection Error. Retrying {kwargs.get('retries')}/{kwargs.get('max_retries')}...")
        elif isinstance(e, (TimeoutError )):
            logging.warning(f"Timed out: {e}")
        else:
            logging.warning(f"Error: {e}")
            logging.warning(f"{type(e)}")
    
    async def on_success(*args, **kwargs):
        logging.info("Request succeeded")
        r = args[0]
        if r.status_code == 200:
            logging.info(r.json())
    
    async def on_failure(*args, **kwargs):
        e = args[0]
        logging.error(f"Request failed: {e}")
    
    @retry_on_exception(on_retry=on_retry, on_success=on_success, on_failure=on_failure)
    async def send_request(*args, **kwargs):
        return await curl_cffi.requests.AsyncSession().request(*args, **kwargs)
    
    async def main():
        r = await send_request('GET', 'https://httpbin.org/ip', timeout=5)
        return r
    
    asyncio.run(main())