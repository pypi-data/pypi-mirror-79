from nbmessages.markdown import *

import unittest, os

TESTMD_FILE = '/opt/nbmessages/tests/mocks/test-markdown.md'

class TestMarkdown(unittest.TestCase):
    def test_read_md(self):

        # positive use case
        md_as_str = read_md(TESTMD_FILE)
        assert md_as_str.startswith('#')
        
        with self.assertRaises(FileNotFoundError):
            read_md('/fakepath')
        
        with self.assertRaises(TypeError):
            read_md('/opt/nbmessages/tests/mocks/something.txt')
    
    def test_md2html(self):
        md = read_md(TESTMD_FILE)
        html = md2html(md)
        html.startswith('<h1>')
    

    