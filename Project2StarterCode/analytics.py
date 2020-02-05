from urllib.parse import urlparse
from bs4 import BeautifulSoup


# Stop Words found in (https://www.ranks.nl/stopwords)
# Note: Since we are using Hannah's tokenizer from project one, any special character
# is considered a delimeter so these stop words are adjusted to that.
# (i.e. "they're" will become "they")
# Also in our code, a "WORD" is any sequence of alphanumeric characters that
# is greater than the length of 2, any string less than the length of 2
# is not considered a WORD
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

# Dictionary for each subdomain and their count
subdomains = {}

# longest length subdomain (for formatting purposes)
longgestSubdomain = 0

# records the page/s with the most valid outlinks
most_outlinks = {"page": set(), "total_outlinks": 0}

# keeps track of the page with the most words
most_words = {"page": set(), "total_words": 0}

# Dictionary to keep track of every word in every page together with their frequency
all_words = {}

# longest length word (for formatting purposes)
longestWord = 0


def get_subdomain(url):
    '''
    takes in an absolute path url. The function parses it to get the
    hostname then recording the subdomain and its frequency in a
    dictionary
    '''
    parsed = urlparse(url)
    if "www" in parsed.hostname:
        if subdomains.get(parsed.hostname[4:]):
            subdomains[parsed.hostname[4:]] += 1
        else:
            subdomains[parsed.hostname[4:]] = 1
            isLongerSubdomain(parsed.hostname[4:])
    else:
        if subdomains.get(parsed.hostname):
            subdomains[parsed.hostname] += 1
        else:
            subdomains[parsed.hostname] = 1
            isLongerSubdomain(parsed.hostname)


def isLongerSubdomain(sdm):
    global longgestSubdomain
    if len(sdm) > longgestSubdomain:
        longgestSubdomain = len(sdm)


def check_isGreater(url, num):
    '''
    num is the number of outlink from url. If num is greater than
    most_outlinks["total_outlinks"], then it is replaced by num and
    the url is also replaced
    '''
    if num > most_outlinks["total_outlinks"]:
        most_outlinks["total_outlinks"] = num
        most_outlinks["page"].clear()
        most_outlinks["page"].add(url)
    elif num == most_outlinks["total_outlinks"]:
        most_outlinks["page"].add(url)


def words_tokenizer(TextFilePath):
    '''
    Hannah's tokenizer from project 1.
    in our code, a "WORD" is any sequence of alphanumeric characters that
    is greater than the length of 2, any string less than the length of 2
    is not considered a WORD
    '''
    tokenList = []
    token = []  # v2
    for char in TextFilePath:
        if (char == ''):
            break
        elif (char.isalnum() and ((97 <= ord(char) <= 122) or (65 <= ord(char) <= 90) or (48 <= ord(char) <= 57))):
            token.append(char.lower())  # v2
        else:
            joinedToken = "".join(token)  # v2
            if (joinedToken and len(joinedToken) > 2):
                tokenList.append(joinedToken)  # tokenList.append(token)
            token = []
    return tokenList


def longest_words(url, html_doc):
    '''
    counts the number of words found in url's html_doc.
    Updates most_words dictionary if the html_doc has more words
    than the current documented one.
    Also, records all the words together with its frequency in all_words dictionary
    '''
    soup = BeautifulSoup(html_doc, 'html.parser')
    tokens = words_tokenizer(soup.get_text())
    lenT = len(tokens)
    if lenT > most_words["total_words"]:
        most_words["total_words"] = lenT
        most_words["page"].clear()
        most_words["page"].add(url)
    elif lenT == most_words["total_words"]:
        most_words["page"].add(url)

    record_word(tokens)


def record_word(tokenList):
    '''
    records all the words together from a token list with its frequency in all_words dictionary
    '''
    for token in tokenList:
        if token not in stop_words:
            if all_words.get(token):
                all_words[token] += 1
            else:
                all_words[token] = 1


def printTopFifty(file, tokenMappedFrequencies):
    '''
    prints top 50 words from the all_words dictionary.
    In our code, a "WORD" is any sequence of alphanumeric characters that
    is greater than the length of 2, any string less than the length of 2
    is not considered a WORD
    '''
    sortedTokens = sorted(tokenMappedFrequencies.items(),
                          key=lambda p: (-p[1], p[0]))
    findLongestWord(sortedTokens)

    count = 0
    file.write(
        "50 MOST COMMON WORDS IN THE ENTIRE SET OF PAGES (not including stop words)\n")
    sub1 = longestWord - len("WORD")
    file.write("WORD" + '        ' + ' ' * sub1 + "COUNT\n")
    for pair in sortedTokens:
        sub = longestWord - len(pair[0])
        # print(str(count + 1) + ") " + pair[0] + '\t\t' + str(pair[1]))
        if count < 9:
            file.write("0" + str(count + 1) + ") " +
                       pair[0] + '    ' + ' ' * sub + str(pair[1]) + "\n")
        else:
            file.write(str(count + 1) + ") " +
                       pair[0] + '    ' + ' ' * sub + str(pair[1]) + "\n")
        count += 1
        if count == 50:
            break


def findLongestWord(map):
    global longestWord
    count = 0
    for elem in map:
        if len(elem[0]) > longestWord:
            longestWord = len(elem[0])
        count += 1
        if count == 50:
            break


def printSubdomainCount(file, subdomainMap):
    '''
    prints subdomain dictionary in a nice format
    '''
    sortedTokens = sorted(subdomainMap.items(),
                          key=lambda p: (-p[1], p[0]))

    file.write("Main Domain: .uci.edu\n")
    sub1 = (longgestSubdomain - len("SUBDOMAIN")) - 6
    file.write("SUBDOMAIN" + ' ' * sub1 + "COUNT\n")
    for pair in sortedTokens:
        # print(pair[0][:-8] + '\t\t' + str(pair[1]))
        lenSub = len(pair[0])  # len(pair[0][:-8])
        sub = (longgestSubdomain - lenSub)
        file.write(pair[0][:-8] + "  " + ' ' * sub + str(pair[1]) + "\n")


def printMostOutlinks(file, outMap):
    '''
    prints most_outlinks dictionary in a nice format
    '''
    file.write("The following page/s have the most valid outlinks:\n")
    for elem in outMap["page"]:
        file.write("--->  " + elem + "\n")
    file.write("TOTAL outlinks: " + str(outMap["total_outlinks"]) + "\n")


def printMostWords(file, wordMap):
    '''
    prints most_words dictionary in a nice format
    '''
    file.write("The following page/s have the most words:" + "\n")
    for elem in wordMap["page"]:
        file.write("--->  " + elem + "\n")
    file.write("TOTAL number of words: " + str(wordMap["total_words"]) + "\n")


def display_analytics(file):
    '''
    function that prints all analytics
    '''
    file.write("this file contains ANALYTICS SPECIFICATIONS' 1,2,4 and 5\n")
    file.write("1: Keep track of the subdomains that it visited, and count\n\thow many different URLs it has processed from each\n\tof those subdomains.\n")
    file.write(
        "2: Find the page with the most valid out links\n\t(of all pages given to your crawler).\n")
    file.write(
        "4: What is the longest page in terms of number of words?\n\t(HTML markup doesn’t count as words).\n")
    file.write("5: What are the 50 most common words in the entire set of pages?\n\t(Ignore English stop words, which can be found,\n\t(https://www.ranks.nl/stopwords).\n\n\n")

    printSubdomainCount(file, subdomains)
    file.write("\n\n" + "*" * 30 + "\n")
    file.write("*" * 30 + "\n\n")
    printMostOutlinks(file, most_outlinks)
    file.write("\n\n" + "*" * 30 + "\n")
    file.write("*" * 30 + "\n\n")
    printMostWords(file, most_words)
    file.write("\n\n" + "*" * 30 + "\n")
    file.write("*" * 30 + "\n\n")
    printTopFifty(file, all_words)
