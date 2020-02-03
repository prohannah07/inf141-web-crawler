import atexit
import atexit
import logging

import sys

# import re
# from urllib.parse import urlparse

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

    # https://www.ics.uci.edu/~sjordan/research/device attachment.html
    # https://grape.ics.uci.edu/wiki/asterix/raw-attachment/wiki/stats170ab-2018/postgresloading.sql
    # parsed = urlparse("https://grape.ics.uci.edu/wiki/asterix/raw-attachment/wiki/stats170ab-2018/postgresloading.sql")
    # print(parsed)
    # if ".ics.uci.edu" in parsed.hostname :
    #     print("Grape in Hostname")
    # if re.match("^.*attachment.*$", parsed.path.lower()):
    #     print("Also Attachment")
    # parsed = urlparse("https://grape.ics.uci.edu/wiki/asterix/timeline?from=2018-04-02T15%3A21%3A31-07%3A00&precision=second")
    # print(parsed)
    # if ".ics.uci.edu" in parsed.hostname :
    #     print("Grape in Hostname")
    # if re.match("^.*timeline.*$", parsed.path.lower()):
    #     print("Also Timeline")
    # parsed = urlparse("https://www.ics.uci.edu/~minhaenl/MH/MHP2G/MHP2G%20v1.2.htm")
    # print(parsed)
    # parsed = urlparse("https://www.ics.uci.edu/~emilyo/teaching/info122w2014/samplecode/lecture8/AbstractFactory/src/NYPizzaStore.java")
    # print(parsed)
    # parsed = urlparse("https://www.ics.uci.edu/~emilyo/teaching/info122w2014/samplecode/lecture8/FactoryMethod/.settings/org.eclipse.jdt.core.prefs")
    # print(parsed)
    # parsed = urlparse("https://www.ics.uci.edu/~emilyo/teaching/info122w2014/samplecode/lecture8/FactoryMethod/bin/PizzaStore.class")
    # print(parsed)
    # parsed = urlparse("http://flamingo.ics.uci.edu/releases/3.0/src/stringmap/split_l.h")
    # print(parsed)
    # parsed = urlparse("http://flamingo.ics.uci.edu/releases/3.0/src/topk/example.cc")
    # print(parsed)
    # parsed = urlparse("http://flamingo.ics.uci.edu/releases/4.1/src/filtertree/data/.svn/entries")
    # print(parsed)

    # file_path = 'stats.txt'

    # fp = open(file_path, 'w')

    analytics_path1 = 'analytics_part1.txt'
    analytics_path2 = 'analytics_part2.txt'
    analytics_path3 = 'analytics_part3.txt'

    ap1 = open(analytics_path1, 'w')
    ap2 = open(analytics_path2, 'w')
    ap3 = open(analytics_path3, 'w')

    crawler = Crawler(frontier, corpus, ap2, ap3)
    crawler.start_crawling()

    # fp.close()

    analytics.display_analytics(ap1)

    ap1.close()
    ap2.close()
    ap3.close()
