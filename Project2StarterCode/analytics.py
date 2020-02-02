import logging
import re
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import lxml
import tldextract

subdomains = {}
most_outlinks = {"page": set(), "total": 0}


def get_subdomain(url):
    parsed = urlparse(url)
    if "www" in parsed.hostname:
        # print(parsed.hostname[4:])
        if subdomains.get(parsed.hostname[4:]):
            subdomains[parsed.hostname[4:]] += 1
        else:
            subdomains[parsed.hostname[4:]] = 1
    else:
        # print(parsed.hostname)
        if subdomains.get(parsed.hostname):
            subdomains[parsed.hostname] += 1
        else:
            subdomains[parsed.hostname] = 1


def check_isGreater(url, num):
    if num > most_outlinks["total"]:
        most_outlinks["total"] = num
        most_outlinks["page"].clear()
        most_outlinks["page"].add(url)
    elif num == most_outlinks["total"]:
        most_outlinks["page"].add(url)
    print(most_outlinks)
