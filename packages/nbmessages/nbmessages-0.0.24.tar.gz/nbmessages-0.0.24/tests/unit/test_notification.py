import unittest, datetime, os

from nbmessages.notification import Notification
from nbmessages import APPLICATION_DATA_DIR

class TestNotification(unittest.TestCase):
    def setUp(self):
        os.system(f'mkdir {os.path.join(APPLICATION_DATA_DIR, "test")}')
        self.notification = Notification('test', True, datetime.datetime(2050, 1, 2))
    
    def tearDown(self):
        os.system(f'rm -rf {os.path.join(APPLICATION_DATA_DIR, "test")}')
    
    def test_convert_to_dict(self):
        as_dict = dict(self.notification)
        
        assert isinstance(as_dict, dict)
        assert as_dict['expiration_date'] == 'Sun, 02 Jan 2050 12:00:00 UTC'
        assert as_dict['message_board'] == 'test'
        
    def test_expiration_date_throws_if_not_datetime(self):
        with self.assertRaises(TypeError):
            self.notification.expiration_date = 'something'