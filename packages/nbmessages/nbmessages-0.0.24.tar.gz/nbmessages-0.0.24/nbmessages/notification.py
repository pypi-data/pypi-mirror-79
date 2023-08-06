"""Classes/functions related to notification"""

import os, datetime

from oo_tools.save import Saver

from . import APPLICATION_DATA_DIR
from .utils import random_string

class Notification(Saver):
    def __init__(self, message_board, notify=False, expiration_date=datetime.datetime.now()):
        self.notify = True
        self.expiration_date = expiration_date
        self.message_board = message_board
        self.filepath = os.path.join(APPLICATION_DATA_DIR, message_board, 'notify.obj')
        self.notification_id = random_string()
        
    @property
    def expiration_date(self):
        return self._expiration_date
    
    @expiration_date.setter
    def expiration_date(self, expiration_date):
        if not isinstance(expiration_date, datetime.datetime):
            raise TypeError('expiration_date must be datetime')
        
        self._expiration_date = expiration_date
        
    @property
    def base_datetime_format(self):
        return '%a, %d %b %Y'
    
    @property
    def full_datetime_format(self):
        return '%a, %d %b %Y %X %Z'
    
    def __iter__(self):
        yield 'notify', self.notify
        yield 'message_board', self.message_board
        yield 'expiration_date', self.expiration_date.strftime('%a, %d %b %Y') + ' 12:00:00 UTC'
        yield 'notification_id', self.notification_id
        yield 'datetime_format', self.full_datetime_format