from nbmessages.message import *
from nbmessages import APPLICATION_DATA_DIR

import unittest, os, string, random, shutil, bs4

from . import BaseTester

class TestMessage(BaseTester):
    def setUp(self):
        self.setup_dir()
        
        self.message = Message(self.message_board, "# My title\nis awesome", "Foo Bar")
    
    def test_render(self):
        html = self.message.render()
        soup = bs4.BeautifulSoup(html, features='html.parser')
        
        # TODO increase robustness. This is a simple check...
        assert str(soup.h1) == '<h1>My title</h1>'
        
    def tearDown(self):
        self.rm_dir()


class TestMessageContainer(BaseTester):
    def setUp(self):
        # mock the dir
        self.setup_dir()
        
        # inject dummy data
        self.message_container = MessageContainer('test')
        self.body = '# Some message\nYes'
        self.author_id = "Foo Bar"
        self.message_id = 'test'
        self.message = Message(self.message_id, self.body, author=self.author_id)
        self.message_container.append(self.message)
        
        assert len(self.message_container) == 1
    
    def tearDown(self):
        self.rm_dir()
    
    def test_message_ids(self):
        assert self.message_container.message_ids == [self.message_id]
    
    def test_get_message_ids(self):
        assert self.message == self.message_container.get(self.message_id)
        
    def test_append(self):
        with self.assertRaises(FileExistsError):
            self.message_container.append(self.message)
        
    def test_delete(self):
        mid = 'id1'
        new_message = Message(mid, 'some body', 'Foo Bar')
        self.message_container.append(new_message)
        
        assert len(self.message_container) == 2
        
        self.message_container.delete(mid)
        
        assert len(self.message_container) == 1
        
        assert mid not in self.message_container.message_ids
        
    