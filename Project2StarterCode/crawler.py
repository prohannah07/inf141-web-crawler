import logging
import re
from urllib.parse import urlparse
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import lxml

logger = logging.getLogger(__name__)

class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier, corpus, file):
        self.frontier = frontier
        self.corpus = corpus
        self.file = file

    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched, len(self.frontier))
            url_data = self.corpus.fetch_url(url)

            for next_link in self.extract_next_links(url_data):
                if self.is_valid(next_link):
                    if self.corpus.get_file_name(next_link) is not None:
                        self.frontier.add_url(next_link)

    def extract_next_links(self, url_data):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.

        Suggested library: lxml
        """
        #outputLinks = ["https://www.ics.uci.edu/about/", "https://www.ics.uci.edu/about/equity/"]
        outputLinks = []
        '''
        print("url: " + url_data["url"])
        if url_data["content"] is None:
            print("content: None")
        else:
            print("content: some binary file")
        print("size: " + str(url_data["size"]))
        print("content_type: " + str(url_data["content_type"]))
        print("http_code: " + str(url_data["http_code"]))
        print("is_redirected: " + str(url_data["is_redirected"]))
        print("final_url: " + str(url_data["final_url"]))
        '''
        #self.file.write("------------------------------------------")
        self.file.write(url_data['final_url']) if url_data['is_redirected'] == True else self.file.write(url_data['url'])
        #self.file.write("------------------------------------------")
        self.file.write("\n")
        soup = BeautifulSoup(url_data["content"], 'lxml-xml')
        for link in soup.find_all('a', href=True):
            extracted_link = link.get('href')
            if "http" not in extracted_link:
                #print(link.get('href'))
                if url_data["is_redirected"] == True:
                   web_url = url_data["final_url"]
                   extracted_link = urljoin(web_url,extracted_link)
                   #self.file.write(urljoin(web_url,extracted_link))
                   #self.file.write("\n")
                else:
                    web_url = url_data["url"]
                    extracted_link = urljoin(web_url,extracted_link)
                    #self.file.write(urljoin(web_url,extracted_link))
                    #self.file.write("\n")
            outputLinks.append(extracted_link)
        return outputLinks
        '''
                if url_data["is_redirected"] == True:
                    self.file.write(url_data['url'])
                    self.file.write("  --------->  ")
                    self.file.write(url_data['final_url'])
                    self.file.write("\n")
                else:
                    self.file.write(url_data['url'])
                    self.file.write("\n")
                #print(link.get('href'))

                #print(soup.get_text())
        ''' 
        

    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        """
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        try:
            return ".ics.uci.edu" in parsed.hostname \
                   and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                                    + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                                    + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                                    + "|thmx|mso|arff|rtf|jar|csv" \
                                    + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

        except TypeError:
            print("TypeError for ", parsed)
            return False

