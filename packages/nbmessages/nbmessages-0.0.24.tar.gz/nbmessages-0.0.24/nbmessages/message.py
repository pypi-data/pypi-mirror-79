"""Object representations of message(s)"""

import os, time

from typing import List
from oo_tools.save import Saver

from . import APPLICATION_DATA_DIR
from .markdown import md2html, decorate_message

import datetime, abc, logging


class Message:
    """Object representation of a message"""

    def __init__(self, message_id, body=None, author=None, base_url='/', is_active=True, color_scheme='nbmessage-default'):
        self.author = author
        self.timestamp = datetime.datetime.now().astimezone()
        self.body = body
        self.base_url = base_url
        self.message_id = message_id
        self.is_active = is_active
        self.color_scheme = color_scheme
    
    @property
    def timestamp_str(self):
        return self.timestamp.strftime('%a, %b %Y,  %H:%M %p %Z')

    def render(self):
        html = md2html(self.body)
        html = decorate_message(html, self.author, self.timestamp_str, self.base_url, self.color_scheme)
        return html


class MessageContainer(Saver):
    """Proxy class for interacting with messages. Acts like a list"""
    
    def __init__(self, subdir):
        self.messages: List[Message] = []
        self.subdir = subdir
        self.filepath = os.path.join(APPLICATION_DATA_DIR, subdir, 'message_container.obj')
    
    def __iter__(self):
        for message in self.messages:
            yield message
    
    def __len__(self):
        return len(self.messages)

    @property
    def message_ids(self):
        return [message.message_id for message in self.messages]
    
    def append(self, message: Message):
        if not isinstance(message, Message): raise TypeError(f'message must be of type Message, not = {type(message)}')
        if message.message_id in self.message_ids: raise FileExistsError(f'message_id = {message.message_id} already exists inside the container, so cannot add it')
        
        self.messages.append(message)
    
    def get(self, message_id):
        for message in self.messages:
            if message.message_id == message_id:
                return message
        
        raise FileNotFoundError(f'Could not find message object with ID = {message_id}')
    
    def sort(self):
        self.messages = sorted(
            self.messages,
            key=lambda x: x.timestamp, reverse=True
        )
        
    def delete(self, message_id):
        for i, message in enumerate(self.messages):
            if message.message_id == message_id:
                self.messages.pop(i)
                self.save()
                return
        
        raise FileNotFoundError(f'Could not find message object with ID = {message_id}')
    
    def load_messages(self):
        try:
            self.load()
        except FileNotFoundError:
            logging.info(f'Starting message container for the first time for subdir = {self.subdir}')
    
    def render(self):
        self.sort()
        html = ''
        for message in self.messages:
            html += message.render()
        
        container = f"""
        <div class="container padding-left-sm padding-bottom-sm nbmessage-render">
            {html}
        </div>
        """
        
        return container