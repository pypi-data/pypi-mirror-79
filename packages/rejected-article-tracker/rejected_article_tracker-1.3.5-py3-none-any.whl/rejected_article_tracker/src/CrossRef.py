from .SearchProvider import SearchProvider

import json

import logging
import time

class CrossRef(SearchProvider):
    def __init__(self, article: dict, http_client, sleep, email=''):
        self.article = article
        self.http_client = http_client
        self.sleep = sleep
        self.email = email

    def search(self) -> list:
        """
        Searches CrossRef for matching titles.
        """
        address = "https://api.crossref.org/works/"
        payload = {
            'filter': 'from-created-date:{}'.format(self.article['text_sub_date']),
            'query.bibliographic': self.article['manuscript_title'],
            'query.author': self.article['authors'].split(', '),
            'rows': 10
        }

        headers = {
            'User-Agent': "{} article tracking".format(self.email),
            'mailto': self.email
        }
        logging.info(headers)
        t0 = time.time()
        response = self.http_client.get(address, params=payload, headers=headers)
        t1 = time.time()
        logging.info('TOTAL TIME FOR REQUEST: {}'.format(t1-t0))

        return response.json()['message']['items']
