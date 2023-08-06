from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
from tornado import web
import os, json, logging, datetime

from ...base import get_directories, check_xsrf
from ...utils import *
from ...markdown import *
from ...users import Admin
from ...message import Message, MessageContainer
from ...notification import Notification
from ... import CONFIG_DIR

class AdminHandler(IPythonHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        yaml = load_yaml(os.path.join(CONFIG_DIR, 'nbmessages-config.yaml'));
        title = yaml.pop('tab_title')
        self.write(json.dumps(title)) 
class MessagesHandler(IPythonHandler):

    def _preview_message(self):
            admin = Admin(self.message_board)
            message = Message(self.body['message_id'], 
                              self.body['message_body'], 
                              self.body['author'], 
                              base_url=self.body['base_url'], 
                              color_scheme=f'nbmessage-{self.body["color_scheme"].lower()}'
                              )
    
            admin.messages.append(message)
            self.write(admin.messages.render())
            
    def _check_notification(self):
        """check whether a notification needs to be created, if it does, create it. If there's a problem with the inputs,
        return boolean False, else return True

        Returns:
            [bool]: False if everything checks out, True otherwise
        """
        try:
            # FIXME vet this logic
            # NO expiration date specified, but wants notification
            notify = self.body['set_notification'] == 'on'
            # if self.body['expiration_date'] != '':
            #     self.set_status(400)
            #     self.finish(f'Only specify a date if you want to add a notification')
            #     return True
    
            

            if notify and self.body['expiration_date'] == '':
                self.set_status(400)
                self.finish(f'You must specify an expiration date if you want a notification')
                return True

            if not notify:
                return False
            
            expiration_date = datetime.datetime.strptime(self.body['expiration_date'], '%m/%d/%Y')
            now = datetime.datetime.now()

                        
            # expiration date is too low
            if now > expiration_date:
                self.set_status(400)
                self.finish('Expiration date must be greater than the date now')
                return True
            
            notification = Notification(self.message_board, notify=True, expiration_date=expiration_date)
            notification.save('0755')
            return False
        
        except KeyError:
            # happens when notify is not set
            return False

        except ValueError:
            # it's not a date
            self.set_status(400)
            self.finish(f'Date must be a date with format MM/DD/YYYY')
            
    def _submit_message(self):
        try:
            # update the message object
            body = self.body
            admin = Admin(self.message_board)
            admin.messages.load_messages()
            
            # check message id
            message_ids = admin.messages.message_ids

            if body['message_id'] in message_ids:
                self.set_status(400)
                self.finish(f"message_id = {body['message_id']} already exist!")
                return
            
            # check if a notification has been requested
            if self._check_notification():
                # notification inputs invalid
                return

            # finally create the message
            message = Message(body['message_id'], body['message_body'], body['author'], base_url=body['base_url'], color_scheme=f'nbmessage-{body["color_scheme"].lower()}')
            admin.messages.append(message)
            admin.messages.sort()
            admin.messages.save()
            
            admin.save_message_file()
            self.write(f'message_id = {body["message_id"]} has been saved.')
        
        except PermissionError:
            self.set_status(400)
            self.finish(f'You dont have permissions to create messages for message board = {self.message_board}')
        
    @web.authenticated
    @check_xsrf
    def post(self, message_board):
        """posting to this server route follows this procedure
        
            1. preview the message
            2. check the form for anything that needs to be checked server side and submit it
        """
        
        # setup variables needed by helper functions
        body = json.loads(self.request.body.decode('utf-8'))
        self.message_board = message_board
        self.body = body
        
        # check that the directory exists first
        message_boards = get_directories()
        if message_board not in message_boards:
            raise web.HTTPError(404, f"Directory = {message_board} doesnt exist!")

        if body['operation'] == 'add' and body['status'] == 'preview':
            # preview
            self._preview_message()
        
        elif body['operation'] == 'add' and body['status'] == 'submit':
            self._submit_message()

    @web.authenticated
    @check_xsrf
    def delete(self, message_board):
        try:
            body = json.loads(self.request.body.decode('utf-8'))
            admin = Admin(message_board)
            result = admin.delete_message(body['message_id'])
            keys = result.keys()
            
            if 'error' in keys:
                self.write(f'<p class="alert alert-danger">{result["error"]}</p>')
            
            else:
                self.write(f'<p class="alert alert-success">{result["success"]}</p>')
    
        except Exception as e:
            logging.error(e)
            self.write({'error': str(e)})
    
    @web.authenticated
    @check_xsrf
    def get(self, message_board):
        admin = Admin(message_board)
        data = admin.get_messages_for_delete()
        return self.write(json.dumps(data))
            
class DirectoryHandler(IPythonHandler):
    @web.authenticated
    def get(self):
        message_boards = get_directories()
        self.write(json.dumps(message_boards))

def load_jupyter_server_extension(nbapp):
    """
    Called during notebook start
    """
    route_pattern = url_path_join(nbapp.web_app.settings['base_url'], '/nbmessage')
    nbapp.web_app.add_handlers('.*', [
        (url_path_join(route_pattern, '/admin'), AdminHandler),
        (url_path_join(route_pattern, '/directories'), DirectoryHandler),
        (url_path_join(route_pattern, r'/messages/(\w+)'), MessagesHandler)
    ])
