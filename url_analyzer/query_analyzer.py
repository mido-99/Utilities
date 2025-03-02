import requests
from curl_cffi import requests as curl_requests
from urllib.parse import urlparse, parse_qs, quote
import json

class UrlAnalyzer:
    
    def __init__(self, url, **kwargs):
        self.url = url
        self.method = 'GET'
        self.params = None
        self.headers = None
        self.cookies = None
        self.json = None
        self.data = None
        self.timeout = 30
        self.impersonate = 'chrome124'
        self.http_client = requests

        for k, v in kwargs.items():
            self.__setattr__(k, v)
    
    def send_request(self):
        self.response = requests.request(
            self.method,
            self.url,
            params=self.params,
            data=self.data,
            json=self.json,
            headers=self.headers,
            cookies=self.cookies,
            timeout=self.timeout,
        )
    
    def send_curl(self):
        self.response = curl_requests.request(
            self.method,
            self.url,
            params=self.params,
            data=self.data,
            json=self.json,
            headers=self.headers,
            cookies=self.cookies,
            timeout=self.timeout,
        )
    
    def url_analyze(self):
        url_split = urlparse(self.url)
        
        interest = [url_split]
        for i in interest:
            print(i)
            print('#'* 40)
    
    def api_analyze(self):
        if self.http_client == curl_requests:
            self.send_curl()
        else:
            self.send_request()
        return self.response

    
analyzer = UrlAnalyzer(
    'https://example.com'
)

analyzer.url_analyze()