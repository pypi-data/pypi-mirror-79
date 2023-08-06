from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler, AuthenticatedFileHandler
from tornado import web
import json, os

from ...base import get_directories, check_xsrf
from ...users import Basic
from ... import APPLICATION_DATA_DIR, STATIC_DIR


class ShowMessage(IPythonHandler):
    @web.authenticated
    @check_xsrf
    def get(self, message_board):
        mounted_directories = get_directories()
        if message_board in mounted_directories:
            try:
                with open(os.path.join(APPLICATION_DATA_DIR, message_board, 'messages.html'), 'r') as f:
                    html = f.readlines()
                    html = ''.join(html)
                
                response = {'html': html}
                
                self.write(json.dumps(response))
            except Exception as e:
                self.write(json.dumps({'html': '<div class="container nbmessage-render">No messages yet</div>'}))
    
        else:
            raise web.HTTPError(404, f"Directory = {message_board} doesnt exist!")
        
class Notify(IPythonHandler):
    @web.authenticated
    @check_xsrf
    def get(self):
        basic = Basic()
        notification = basic.get_youngest_notification()
        self.write(json.dumps(notification))        

def load_jupyter_server_extension(nbapp):
    """
    Called during notebook start
    """
    route_pattern = url_path_join(nbapp.web_app.settings['base_url'], '/nbmessage')
    nbapp.web_app.add_handlers('.*', [
        (url_path_join(route_pattern, r'/render/(\w+)'), ShowMessage),
        (url_path_join(route_pattern, r'/notify'), Notify),
        (route_pattern + '/(.*)', web.StaticFileHandler, {'path': f'{STATIC_DIR}'})
    ])
    # FIX ME move to top
    # nbapp.web_app.add_handlers('.*', [(route_pattern + '/(.*)', web.StaticFileHandler, {'path': f'{STATIC_DIR}'})])