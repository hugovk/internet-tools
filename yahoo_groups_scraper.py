#!/usr/bin/env python
# encoding: utf-8
"""
Yahoo! Groups! Scraper!

Because! Yahoo's! Advanced! Search! Doesn't! Work!
    "Oops! Sorry, an error occurred while loading the content."
Scrape! 'Em! And! Search! Locally! Instead!
"""
from __future__ import print_function
import argparse
from bs4 import BeautifulSoup  # pip install BeautifulSoup4
import os.path
import urllib2
from urlparse import urljoin  # Python 2

# from pprint import pprint


def download_topic(url):
    """
    Save a topic (with possibly more than one message) to file,
    then return the URL of the next topic
    """
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page.read(), "lxml")

    # pprint(soup)

    # Possibly multiple messages per topic stored in a:
    # <ul class="msg-list-container" ... >
    #   <li class="yg-msg-read-container  clrfix card" ... >
    # But let's just save the <ul>

    topic = soup.find_all("ul", class_="msg-list-container")[0]

    # Each message has a data-msgid; let's use the first message's data-msgid
    # to store the whole topic
    messages = topic.find_all("li", class_="yg-msg-read-container")
    data_uid = messages[0]['data-msgid']
    data_uid = data_uid.zfill(6)
    outfile = os.path.join(args.outdir, data_uid + ".html")

    if os.path.isfile(outfile):
        print("Skip:", outfile)
    else:
        print("Save:", outfile)
        with open(outfile, "w") as file:
            file.write(str(topic))
            file.write('<P>Link to original: <a href="' + url + '">"' + url +
                       '</a>')

    # Find next topic
    next_prev_links = soup.find_all("a", class_="msg-read-prev-next")[0]
    href = next_prev_links['href']
    if not href.startswith("http"):
        href = urljoin(url, href)

    return href


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Yahoo! Groups! Scraper!",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-s', '--start_url',
        default='https://groups.yahoo.com/neo/groups/ipodder-dev/'
                'conversations/topics/1',
        help="URL of first topic to start scraping from")
    parser.add_argument(
        '-o', '--outdir', default='words/ipodder-dev',
        help="Directory where topics will be saved")
    args = parser.parse_args()

    next_url = args.start_url
    print("Start:", next_url)
    while(True):
        next_url = download_topic(next_url)
        print("Next:", next_url)

# End of file
