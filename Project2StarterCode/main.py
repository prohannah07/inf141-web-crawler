import atexit
import atexit
import logging

import sys

import re
from urllib.parse import urlparse

from corpus import Corpus
from crawler import Crawler
from frontier import Frontier

import analytics

if __name__ == "__main__":
    # Configures basic logging
    logging.basicConfig(format='%(asctime)s (%(name)s) %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                        level=logging.INFO)

    # Instantiates frontier and loads the last state if exists
    frontier = Frontier()
    frontier.load_frontier()

    # Instantiates corpus object with the given cmd arg
    corpus = Corpus(sys.argv[1])

    # Registers a shutdown hook to save frontier state upon unexpected shutdown
    atexit.register(frontier.save_frontier)

    # Instantiates a crawler object and starts crawling

    analytics_path1 = 'analytics_part1.txt'
    analytics_path2 = 'analytics_part2.txt'
    analytics_path3 = 'analytics_part3.txt'

    ap1 = open(analytics_path1, 'w')
    ap2 = open(analytics_path2, 'w')
    ap3 = open(analytics_path3, 'w')

    crawler = Crawler(frontier, corpus, ap2, ap3)
    crawler.start_crawling()

    analytics.display_analytics(ap1)

    ap1.close()
    ap2.close()
    ap3.close()
