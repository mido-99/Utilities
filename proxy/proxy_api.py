from typing import Any
from dataclasses import dataclass
import random
from urllib.parse import urlparse


@dataclass
class ProxyUrl:
    """Provides unified interface for proxies, returns proxy in format supported by different libraries
    ### Usage
    - Playwright
    
    ```py
    proxy = ProxyUrl('http://bob:password@proxy1.example.com:8000')
    print(proxy.get_playwright_format())
    ```
    returns ``` {'server': 'http://proxy1.example.com:8000', 'username': 'bob', 'password': 'password'}``` 
    """
    url: str | None = None
    
    def __post_init__(self):
        self.parsed = urlparse(self.url.strip())
        self.scheme = self.parsed.scheme  # e.g., "http" or "socks5"
        self.host = self.parsed.hostname  # e.g., "proxy1.example.com"
        self.port = self.parsed.port      # e.g., 8000
        self.username = self.parsed.username  # e.g., "bob"
        self.password = self.parsed.password  # e.g., "password"
    
    def get_playwright_format(self) -> dict[str, Any]:
    
        playwright_proxy = {
            "server": f"{self.scheme}://{self.host}:{self.port}",  # e.g., "http://proxy1.example.com:8000" 
            "username": self.username,  # e.g., "bob"
            "password": self.password   # e.g., "password"
        }
        #! Update to following:
        # "server": "rp.proxyscrape.com:6060",
        # "username 
        # "password
        # Where proxy = "http://mdcOgcjreptyag1:bkb3xjh8xh21evb@xp.proxyscrape.com:6060"
        return playwright_proxy
    
    def get_curl_cffi_format(self)-> dict[str, str]:
        return  {
        "http": self.url,  # Proxy for HTTP
        "https": self.url,  # Proxy for HTTPS
    }
    
    def get_from_pool(self):
        return ProxyUrl(random.choice(self.pool))
