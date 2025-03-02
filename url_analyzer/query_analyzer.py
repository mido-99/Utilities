import requests
from curl_cffi import requests as curl_requests
from urllib.parse import urlparse, parse_qs
import json
from rich import print_json, print

class UrlAnalyzer:
    
    def __init__(self, **kwargs):
        self.url = None
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
        
        for field in url_split._fields:
            value = getattr(url_split, field)
            print(f"{field}: {value}")
            print('-' * 40)
        
        if query := parse_qs(url_split.query):
            print('#'*20, 'Query', '#'*20)
            for k, v in query.items():
                print(f'{k}: {v}')
    
    def data_analyze(self):
        if not self.data:
            raise ValueError('Enter data to analyze!')
        print_json(self.data)
    
    def api_analyze(self):
        if self.http_client == curl_requests:
            self.send_curl()
        else:
            self.send_request()
        return self.response


analyzer = UrlAnalyzer(
    url='https://45bwzj1sgc-dsn.algolia.net/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%3B%20JS%20Helper%20(3.16.1)&x-algolia-application-id=45BWZJ1SGC&x-algolia-api-key=MjBjYjRiMzY0NzdhZWY0NjExY2NhZjYxMGIxYjc2MTAwNWFkNTkwNTc4NjgxYjU0YzFhYTY2ZGQ5OGY5NDMxZnJlc3RyaWN0SW5kaWNlcz0lNUIlMjJZQ0NvbXBhbnlfcHJvZHVjdGlvbiUyMiUyQyUyMllDQ29tcGFueV9CeV9MYXVuY2hfRGF0ZV9wcm9kdWN0aW9uJTIyJTVEJnRhZ0ZpbHRlcnM9JTVCJTIyeWNkY19wdWJsaWMlMjIlNUQmYW5hbHl0aWNzVGFncz0lNUIlMjJ5Y2RjJTIyJTVE',
    data = '{"requests":[{"indexName":"YCCompany_production","params":"facetFilters=%5B%5B%22batch%3AS22%22%2C%22batch%3AS24%22%5D%2C%5B%22regions%3AUnited%20Kingdom%22%5D%5D&facets=%5B%22app_answers%22%2C%22app_video_public%22%2C%22batch%22%2C%22demo_day_video_public%22%2C%22industries%22%2C%22isHiring%22%2C%22nonprofit%22%2C%22question_answers%22%2C%22regions%22%2C%22subindustry%22%2C%22top_company%22%5D&hitsPerPage=1000&maxValuesPerFacet=1000&page=0&query=&tagFilters="},{"indexName":"YCCompany_production","params":"analytics=false&clickAnalytics=false&facetFilters=%5B%5B%22regions%3AUnited%20Kingdom%22%5D%5D&facets=batch&hitsPerPage=0&maxValuesPerFacet=1000&page=0&query="},{"indexName":"YCCompany_production","params":"analytics=false&clickAnalytics=false&facetFilters=%5B%5B%22batch%3AS22%22%2C%22batch%3AS24%22%5D%5D&facets=regions&hitsPerPage=0&maxValuesPerFacet=1000&page=0&query="}]}',
    method="POST"
)

# analyzer.url_analyze()
# analyzer.data_analyze()
print(analyzer.api_analyze())