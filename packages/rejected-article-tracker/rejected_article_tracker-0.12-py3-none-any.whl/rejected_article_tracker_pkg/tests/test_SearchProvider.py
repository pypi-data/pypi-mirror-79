import unittest
from rejected_article_tracker_pkg.src import SearchProvider


class TestSearchProvider(unittest.TestCase):
    def test__search_provider_class_is_empty(self):
        res = SearchProvider().search()
        self.assertTrue(len(res) == 0)


