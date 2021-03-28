import asyncio
from urllib.parse import urlsplit
from typing import Dict, Union, Tuple
from time import time
import random


class RateLimiter:
    def __init__(self, default_rate_limit: Union[float, Tuple[float]] = None,
                 domain_requests_per_sec: Dict[str, Union[float, Tuple[float]]] = None):
        self.default_rate_limit = default_rate_limit
        self.domain_requests_per_sec: Dict[str, float] = {}
        self.time_last_request: Dict[str, int] = {}
        if domain_requests_per_sec is not None:
            self.set_domain_requests_per_sec(domain_requests_per_sec)

    def set_domain_requests_per_sec(self, domain_requests_per_sec: Dict[str, float]):
        """Map domain name to max requests per second for that domain."""
        for domain, limit in domain_requests_per_sec.items():
            self.domain_requests_per_sec[domain] = {
                'limit': limit, 'lock': asyncio.Lock()}

    async def maybe_sleep(self, url: str):
        domain = re.sub(r'^www\.', '', urlsplit(url).netloc)
        if domain not in self.domain_requests_per_sec:
            if self.default_rate_limit is None:
                return
            self.domain_requests_per_sec[domain] = {
                'limit': self.default_rate_limit, 'lock': asyncio.Lock()}
        async with self.domain_requests_per_sec[domain]['lock']:
            # sleep to not exceed max requests per second.
            await asyncio.sleep(self._sleep_time(domain))
        # record time.
        self.time_last_request[domain] = time()

    def _sleep_time(self, domain: str) -> float:
        if domain not in self.time_last_request:
            # no previous request has been made to this domain, so no need to sleep.
            return 0.0
        rate_limit = self.domain_requests_per_sec[domain]['limit']
        if isinstance(rate_limit, tuple):
            rate_limit = random.uniform(*rate_limit)
        # s/req - time since last request
        return max(0, (1 / rate_limit) - (time() - self.time_last_request[domain]))
