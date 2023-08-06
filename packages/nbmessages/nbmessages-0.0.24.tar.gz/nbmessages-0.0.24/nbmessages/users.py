"""Facades/Composites for handling server operations"""

import os, shutil, json, datetime
from bs4 import BeautifulSoup

from .etc import Config
from .message import MessageContainer, Message
from .markdown import md2html, md2bs4, html2bs4
from .notification import Notification
from .base import get_directories
from . import APPLICATION_DATA_DIR

class Admin:
    def __init__(self, message_board):
        self.message_board = message_board
        self.message_container = MessageContainer(self.message_board)
    
    @property
    def messages(self):
        return self.message_container
    
    def save_message_state(self):
        self.messages.sort()
        self.messages.save()
    
    def add_message(self, message):
        self.messages.append(message)
    
    def save_message_file(self):
        self.message_container.load()
        self.message_container.sort()
        if len(self.message_container) == 0:
            html = '<div class="container nbmessage-render">No messages yet</div>'
        else:
            html = self.message_container.render()
        
        save_path = os.path.join(APPLICATION_DATA_DIR, self.message_board, 'messages.html')
        with open(save_path, 'w') as f:
            f.write(html)
        
        os.system(f'chmod 0744 {save_path}')
            
    def get_messages_for_delete(self):
        try:
            self.message_container.load()
            message_ids = self.message_container.message_ids
            rendered_message_bodies = [self.message_container.get(message_id) for message_id in message_ids]
            rendered_message_bodies = [message.render() for message in rendered_message_bodies]
            
            return dict(zip(message_ids, rendered_message_bodies))
        
        except FileNotFoundError:
            return []
    
    def delete_message(self, message_id):
        try:
            self.message_container.load()
            self.message_container.delete(message_id)
            self.message_container.save()
            self.save_message_file()
            return {'success': f'Successfully removed message ID = {message_id}'}

        except PermissionError:
            return {'error': f'Your account doesnt have permissions to delete messages'}
        except FileNotFoundError:
            return {'error': f'could not delete message ID = {message_id}. It doesnt exist!'}
        

class Basic:                
    def _load_notification(self, notification):
        try:
            notification.load()
            return dict(notification)

        except FileNotFoundError:
            return {'notify': False}
        
    def get_youngest_notification(self):
        try:
            message_boards = get_directories()
            notifications = [Notification(message_board) for message_board in message_boards]
            loaded_notifications = [self._load_notification(notification) for notification in notifications]
            
            # filter out notify = false
            filtered_notifications = list(filter(lambda notification: notification != {'notify': False}, loaded_notifications))
            
            if len(filtered_notifications) == 0:
                return {'notify': False}
            
            # find the youngest notification
            youngest_date = datetime.datetime(1980, 1, 1) # some really old starting date
            youngest_notification = None
            for notification in filtered_notifications:
                date = datetime.datetime.strptime(notification['expiration_date'], notification['datetime_format'])
                
                if date > youngest_date:
                    youngest_date = date
                    youngest_notification = notification
            
            return youngest_notification
        
        except PermissionError:
            return {'notify': False}
        
        
        
        