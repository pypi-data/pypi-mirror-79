# from nbmessages.users import *
# from nbmessages.message import Message
# from nbmessages import APPLICATION_DATA_DIR

# import unittest, os, random, bs4

# from . import BaseTester


# class TestAdmin(BaseTester):
#     def setUp(self):
#         self.setup_dir()
#         self.admin = Admin('test')
        
#     def tearDown(self):
#         self.rm_dir()
        
#     def test_add_message(self):
#         assert len(self.admin.message_container) == 0
#         self.admin.add_message('id1', '#My Body', 'Foo Bar', '/')
#         assert len(self.admin.message_container) == 1
    
#     def test_render_messages(self):
#         messages = [self.admin.add_message(f'id{i}', f'#body\n{i}', 'Foo Bar', '/') for i in range(10)]
        
#         html = self.admin.render_messages()
        
#         self.admin.message_container.sort()
#         assert isinstance(html, str)
        
#         # TODO finish testing this        
#         # soup = bs4.BeautifulSoup(html)
#         # print(soup)
        
#         # assert False