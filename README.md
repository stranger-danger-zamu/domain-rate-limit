## Per-domain rate limiting for asynchronous web scraping

### Usage
```python
from domain_rate_limit import RateLimiter
from puppeteer_crawler.spider import Spider

domain_requests_per_sec = {
    'amazon.com': (1.25, 3), # wait between 1/1.25 and 1/3 seconds between dispatching requests to amazon.com
    'ebay.com': 0.33, # wait 1/0.33 seconds between dispatching requests to amazon.com
    'twitter.com': 1, # send 1 request per second to twitter.com
}

rl = RateLimiter(default_rate_limit=(1,2), # send between 1 and 2 requests per second to every domain not in domain_requests_per_sec.
                 domain_requests_per_sec=domain_requests_per_sec)
spider = Spider()


async def get(url):
    # maybe_sleep will block if needed in order to not exceed max requests per second for url's domain.
    await rl.maybe_sleep(url)
    resp, page = spider.get(url)
    print(f'[{resp.status}] {url}')
    await spider.set_idle(page)

async def main(urls: List[str]):
    # many tasks can now be created simultaneously without exceeding rate limits.
    asyncio.gather(*[asyncio.create_task(get(url)) for url in urls])
```