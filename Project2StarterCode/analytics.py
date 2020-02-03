# import logging
# import re
from urllib.parse import urlparse
# from urllib.parse import urljoin
from bs4 import BeautifulSoup
# import lxml
# import tldextract
# from nltk import word_tokenize


stop_words = {"a", "about", "above", "after", "again", "against", "all", "am", "an",
              "and", "any", "are", "aren", "as", "at", "be", "because", "been", "before",
              "being", "below", "between", "both", "but", "by", "can", "cannot", "could",
              "couldn", "did", "didn", "do", "does", "doesn", "doing", "don", "down", "during",
              "each", "few", "for", "from", "further", "had", "hadn", "has", "hasn", "have",
              "haven", "having", "he", "he", "he", "he", "her", "here", "here", "hers", "herself",
              "him", "himself", "his", "how", 'how', "i", "i", "i", "i", "i", "if", "in", "into",
              "is", "isn", "it", "it", "its", "itself", "let", "me", "more", "most", "mustn",
              "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other",
              "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan",
              "she", "she", "she", "she", "should", "shouldn", "so", 'some', "such", "than",
              "that", "that", "the", "their", "theirs", "them", "themselves", "then", "there",
              "there", "these", "they", "they", "they", "they", "they", "this", "those", "through",
              "to", "too", "under", "until", "up", "very", "was", "wasn", "we", "we", "we", "we", "we",
              "were", "weren", "what", "what", "when", "when", "where", "where", "which", "while", "who",
              "who", "whom", "why", "why", "with", "won", "would", "wouldn", "you", "you", "you", "you", "you",
              "your", "yours", "yourself", "yourselves"}


subdomains = {}
most_outlinks = {"page": set(), "total_outlinks": 0}
most_words = {"page": set(), "total_words": 0}
all_words = {}


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
    if num > most_outlinks["total_outlinks"]:
        most_outlinks["total_outlinks"] = num
        most_outlinks["page"].clear()
        most_outlinks["page"].add(url)
    elif num == most_outlinks["total_outlinks"]:
        most_outlinks["page"].add(url)
    # print(most_outlinks)
    # print(stop_words)


def words_tokenizer(TextFilePath):
    # file = open(TextFilePath, "r")
    tokenList = []
    # token = ''
    token = []  # v2
    # while True:
    for char in TextFilePath:
        # char = file.read(1)
        # print(char)
        if (char == ''):
            break
        elif (char.isalnum() and ((97 <= ord(char) <= 122) or (65 <= ord(char) <= 90) or (48 <= ord(char) <= 57))):
            # token += char.lower()
            token.append(char.lower())  # v2
        else:
            joinedToken = "".join(token)  # v2
            if (joinedToken and len(joinedToken) > 2):  # if (token != ''):
                tokenList.append(joinedToken)  # tokenList.append(token)
            token = []  # token = ''
    # file.close()
    return tokenList


def longest_words(url, html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    # tokens = PartA.tokenize(soup.get_text())
    tokens = words_tokenizer(soup.get_text())
    lenT = len(tokens)
    if lenT > most_words["total_words"]:
        most_words["total_words"] = lenT
        most_words["page"].clear()
        most_words["page"].add(url)
    elif lenT == most_words["total_words"]:
        most_words["page"].add(url)
    # print(most_words)

    record_word(tokens)

    # tokenMap = PartA.computeWordFrequencies(tokens)
    # print(soup.get_text())
    # print(tokens)
    # print(tokenMap)


def record_word(tokenList):
    for token in tokenList:
        if token not in stop_words:
            if all_words.get(token):
                all_words[token] += 1
            else:
                all_words[token] = 1


def printTopFifty(tokenMappedFrequencies):
    sortedTokens = sorted(tokenMappedFrequencies.items(),
                          key=lambda p: (-p[1], p[0]))
    count = 0
    print("50 MOST COMMON WORDS IN THE ENTIRE SET OF PAGES (not including stop words)")
    print("WORD\t\tCOUNT")
    for pair in sortedTokens:
        print(str(count + 1) + ") " + pair[0] + '\t\t' + str(pair[1]))
        count += 1
        if count == 50:
            break


def printSubdomainCount(subdomainMap):
    sortedTokens = sorted(subdomainMap.items(),
                          key=lambda p: (-p[1], p[0]))

    print("Main Domain: .uci.edu")
    print("SUBDOMAIN\t\tCOUNT")
    for pair in sortedTokens:
        print(pair[0][:-8] + '\t\t' + str(pair[1]))


def printMostOutlinks(outMap):
    print("The following page/s have the most valid outlinks:")
    for elem in outMap["page"]:
        print("--->  " + elem)
    print("TOTAL outlinks: " + str(outMap["total_outlinks"]))


def printMostWords(wordMap):
    print("The following page/s have the most words:")
    for elem in wordMap["page"]:
        print("--->  " + elem)
    print("TOTAL number of words: " + str(wordMap["total_words"]))


def display_analytics():
    printSubdomainCount(subdomains)
    printMostOutlinks(most_outlinks)
    printMostWords(most_words)
    printTopFifty(all_words)
