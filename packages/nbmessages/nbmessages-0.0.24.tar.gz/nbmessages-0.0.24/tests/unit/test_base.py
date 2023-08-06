from nbmessages.base import *
from nbmessages import APPLICATION_DATA_DIR

import unittest, os, sqlite3

NEWDIR = os.path.join(APPLICATION_DATA_DIR, 'test2')

class TestGetDirectories(unittest.TestCase):

    def tearDown(self):
        self.rmdir()
    
    def rmdir(self):
        try:
            os.rmdir(NEWDIR)
        except:
            pass
    
    def test_get_directories(self):
        directories = get_directories()
        
        assert 'sql' not in directories, 'sql is in the directory'
        assert 'test2' not in directories, 'mock directory is listed'
        
        os.mkdir(NEWDIR)
        assert 'test2' in os.listdir(APPLICATION_DATA_DIR), 'test2 has been created in the application directory'
        
        directories = get_directories()
        assert 'test2' in directories, 'mock directory needs to be listed'