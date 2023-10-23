#!/usr/local/bin/python
# coding: utf-8

import unittest
import urllib2
import json
import sys
import re
import os
import random
import string

'''Variety of simple tests to check that nothing is obviously broken'''


class TestIntegration(unittest.TestCase):

    def getData(self, url):
        data = urllib2.urlopen(url)
        self.assertEqual(200, data.getcode())
        data = data.read()
        return data

    def getRandomLetters(self, count):
        return ''.join(random.choice(string.letters) for _ in xrange(count))

    def testMainPage(self):
        data = self.getData(f"http://{host}/")
        result = 'Searching across' in data or 'You have no repositories indexed' in data
        self.assertTrue(result)
        self.assertTrue('Repositories' in data)
        self.assertTrue('Documentation' in data)
        self.assertTrue('Admin' in data)

    def testDocumentationPage(self):
        data = self.getData(f"http://{host}/documentation/")
        self.assertTrue('<h2>Documentation</h2>' in data)

    def testLoginPage(self):
        data = self.getData(f"http://{host}/login/")
        self.assertTrue('Enter Password' in data)

    def testAdminRedirect(self):
        data = self.getData(f"http://{host}/admin/")
        self.assertTrue('Enter Password' in data)

    def testAdminBulkRedirect(self):
        data = self.getData(f"http://{host}/admin/bulk/")
        self.assertTrue('Enter Password' in data)

    def testAdminSettingsRedirect(self):
        data = self.getData(f"http://{host}/admin/settings/")
        self.assertTrue('Enter Password' in data)

    def testJsonLoads(self):
        data = self.getData(f"http://{host}/api/codesearch/?q=test&p=0")
        data = json.loads(data)
        self.assertTrue('totalHits' in data)

    def testSearchJsPreload(self):
        data = self.getData(f"http://{host}/?q=test")
        self.assertTrue('var preload = {' in data)

    def testSearch(self):
        data = self.getData(f"http://{host}/html/?q=test")
        self.assertTrue('Filter Results' in data)

    def testCodeResults(self):
        url = f"http://{host}/file/zeroclickinfo-fathead/lib/fathead/java/test_parse.py"
        data = self.getData(url)
        #self.assertTrue('MD5 Hash' in data)

    def testRepositoryList(self):
        url = f"http://{host}/repository/list/"
        data = self.getData(url)
        self.assertTrue(
            '<script src="/js/intercooler-1.1.2.min.js"></script>' in data)

    def testNoSearch(self):
        url = f"http://{host}/?q=&p=0"
        data = self.getData(url)
        result = 'Searching across' in data or 'You have no repositories indexed' in data
        self.assertTrue(result)

    def testNoSearchHtml(self):
        url = f"http://{host}/html/?q=&p=0"
        self.getData(url)

    def testNoSearchJson(self):
        url = f"http://{host}/api/codesearch/?q=&p=0"
        self.getData(url)

    def testSearchLoad(self):
        for _ in xrange(1000):
            url = f"http://{host}/html/?q={self.getRandomLetters(10)}"
            data = self.getData(url)
            self.assertTrue('No results found' in data)

    def test_index_suggest(self):
        for _ in xrange(1000):
            url = f"http://{host}/api/repo/index/?repoUrl=http://test.com/"
            data = self.getData(url)
            self.assertTrue('Was unable to find repository' in data)

    def test_rss_search(self):
        url = f"http://{host}/api/codesearch/rss/?q=test&p=0"
        data = self.getData(url)
        self.assertTrue('title>Search for "test"</title>' in data)
        self.assertTrue(
            '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">' in data)

    def testCheckResponseHeadersApi(self):
        urls = [
            'api/codesearch/?q=test',
            'api/timecodesearch/?q=test',
            'api/repo/list/',
            'api/repo/add/',
            'api/repo/delete/',
            'api/repo/reindex/',
            'api/repo/index/',
            'api/repo/repo/?reponame=searchcode',
        ]

        for url in urls:
            url = f'http://{host}/{url}'
            data = urllib2.urlopen(url)
            header = data.info().getheader('Content-Type')
            self.assertEqual(header, 'application/json', url)

    def testCheckResponse200(self):
        urls = [
            'api/repo/indextime/?reponame=searchcode',
            'api/repo/filecount/?reponame=searchcode',
            'api/repo/indextimeseconds/?reponame=searchcode',
        ]

        for url in urls:
            url = f'http://{host}/{url}'
            urllib2.urlopen(url)

    def testFuzzyBadData(self):
        self.getData(f"http://{host}/html/?q=test&p=100")
        self.getData(f"http://{host}/html/?q=test&p=a")
        self.getData(f"http://{host}/html/?&p=a")
        self.getData(f"http://{host}/html/?q=test&p=1asds")
        self.getData(f"http://{host}/html/?q=test&p=1&repo=test&lan=test")

        for _ in xrange(1000):
            url = f"http://{host}/html/?{self.getRandomLetters(1)}={self.getRandomLetters(10)}&{self.getRandomLetters(1)}={self.getRandomLetters(10)}"
            self.getData(url)

        for _ in xrange(1000):
            self.getData(
                f"http://{host}/html/?q={self.getRandomLetters(10)}&repo={self.getRandomLetters(10)}&lan={self.getRandomLetters(10)}"
            )


if __name__ == "__main__":
    host = "localhost:8080"
    unittest.main()
