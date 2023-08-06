"""Custom scrapy extensions."""
import logging

from scrapy.extensions.throttle import AutoThrottle

import tldextract


class CustomDelayThrottle(AutoThrottle):
    """Set custom `DOWNLOAD_DELAY`for different domain."""

    def __init__(self, crawler):
        """Initialize the custom delay throttle."""
        self.domain_delays = crawler.settings.getdict('DOMAIN_DELAYS')
        logging.debug('Using Custom AutoThrottle')
        super().__init__(crawler)

    def _adjust_delay(self, slot, latency, response):
        """Override AutoThrottle._adjust_delay()."""
        site_domain = tldextract.extract(response.url).domain
        if site_domain in self.domain_delays:
            if response.status != 200:
                return
            slot.delay = self.domain_delays[site_domain]
        else:
            super()._adjust_delay(slot, latency, response)
