import time, datetime, random, string, os

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from nbmessages import APPLICATION_DATA_DIR

from . import get_driver, BaseAcceptanceTester

class TestMessageCreationSystem(BaseAcceptanceTester):
    # def test_create_message(self):
    #     body = """# What is Lorem Ipsum
        
    #     Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
    #     """

    #     input_name = 'My Name'
    #     self.create_message('mboard', input_name, body, 'm1')
        
    #     # check announcements tab
    #     announcements = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Announcements')))
    #     announcements.click()
        
    #     # check that the mboard tab has the message
    #     mboard_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'mboard')))
    #     mboard_tab.click()
    #     mboard_tab.click()
        
    #     time.sleep(1)
        
    #     soup = self.get_soup()
        
    #     self.driver.save_screenshot('/opt/nbmessages/tests/acceptance/screenshots/admin-mboard.png')
    #     assert soup.find(id='nbmessage-messages') is not None
    #     assert soup.find(text='What is Lorem Ipsum') is not None
    #     assert soup.find(text=input_name) is not None
        
    #     # check that board 'test' doesn't have any messages
    #     test_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'test')))
    #     test_tab.click()
    #     test_tab.click()
        
    #     time.sleep(1)
    #     soup = self.get_soup()
    #     self.driver.save_screenshot('/opt/nbmessages/tests/acceptance/screenshots/admin-test.png')
    #     assert soup.find(text='No messages yet') is not None
        
    # def test_add_multiple_messages(self):
    #     body1 = "# Hello\nThere"
    #     author1 = 'Name1'
    #     id_1 = 'm1'
        
    #     body2 = "# Hi\nThere"
    #     author2 = 'Name2'
    #     id_2 = 'm2'
        
    #     self.create_message(self.board1, author1, body1, id_1)
    #     self.driver.refresh()
    #     self.create_message(self.board1, author2, body2, id_2)
        
    #     # check announcements tab
    #     announcements = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Announcements')))
    #     announcements.click()
        
    #     # check that the mboard tab has the message
    #     mboard_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'mboard')))
    #     mboard_tab.click()
    #     mboard_tab.click()
        
    #     time.sleep(1)
        
    #     soup = self.get_soup()
        
    #     self.driver.save_screenshot('/opt/nbmessages/tests/acceptance/screenshots/admin-mboard-multi.png')
        
    #     assert soup.find(id='nbmessage-messages') is not None
    #     # message 1
    #     assert soup.find(text='Hello') is not None
    #     assert soup.find(text=author1) is not None
        
    #     # message 2
    #     assert soup.find(text='Hi') is not None
    #     assert soup.find(text=author2) is not None
        
    #     # check that board 'test' doesn't have any messages
    #     test_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'test')))
    #     test_tab.click()
    #     test_tab.click()
        
    #     time.sleep(1)
    #     soup = self.get_soup()
    #     assert soup.find(text='No messages yet') is not None
        
    # def test_messages_isolated_between_message_boards(self):
    #     body1 = "# Hello\nThere"
    #     author1 = 'Name1'
    #     id_1 = 'm1'

    #     self.create_message(self.board1, author1, body1, id_1)
    #     self.driver.refresh()
        
    #     body2 = '# Hi\nThere'
    #     author2 = 'Name2'
    #     id_2 = 'm1'

    #     self.create_message(self.board2, author2, body2, id_2)
        
    #     announcements = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Announcements')))
    #     announcements.click()
        
    #     mboard_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'mboard')))
    #     mboard_tab.click()
    #     mboard_tab.click()
        
    #     soup = self.get_soup()
        
    #     self.driver.save_screenshot('/opt/nbmessages/tests/acceptance/screenshots/admin-multi.png')
    #     assert soup.find(id='nbmessage-messages') is not None
    #     # message 1
    #     assert soup.find(text='Hello') is not None
    #     assert soup.find(text=author1) is not None
        
    #     test_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'test')))
    #     test_tab.click()
    #     test_tab.click()
        
    #     soup = self.get_soup()
        
    #     self.driver.save_screenshot('/opt/nbmessages/tests/acceptance/screenshots/admin-multi2.png')
    #     assert soup.find(id='nbmessage-messages') is not None
    #     # message 2
    #     assert soup.find(text='Hi') is not None
    #     assert soup.find(text=author2) is not None
        
    # def test_add_notification(self):
    #     body1 = "# Hello\nThere"
    #     author1 = 'Name1'
    #     id_1 = 'm1'

        
    #     expiration = datetime.datetime(2055, 1, 1) # this will be valid for awhile >:D
    #     expiration = expiration.strftime('%m/%d/%Y')

    #     self.create_message(self.board1, author1, body1, id_1, add_notification=True, expiration_date=expiration) # expiration date
        
    # def test_add_multiple_notifications(self):
    #     letters = string.ascii_lowercase
    #     message_boards = ['test', 'mboard']
    #     messages_in_board = [0, 0]
        
    #     for i in range(10):
    #         # 2 paragraphs essentially
    #         body = ''.join(random.choice(letters) for i in range(300))
    #         body = body + '\n<br/>' + ''.join(random.choice(letters) for i in range(300))
            
    #         author = ''.join(random.choice(letters) for i in range(20))
    #         message_id = ''.join(random.choice(letters) for i in range(10))
            
    #         board = random.randint(0, 1)
    #         message_board = message_boards[board]
            
    #         self.create_message(message_board, author, body, message_id)
    #         messages_in_board[board] += 1
        
    #     announcements = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Announcements')))
    #     announcements.click()
        
    #     mboard_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'mboard')))
    #     mboard_tab.click()
    #     mboard_tab.click()
        
    #     soup = self.get_soup()
    #     mboard_messages = len(soup.select('.nbmessage-border'))
    #     assert mboard_messages == messages_in_board[1]
    #     self.driver.save_screenshot('/opt/nbmessages/tests/acceptance/screenshots/admin-mboard-multi.png')
        
    #     test_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'test')))
    #     test_tab.click()
    #     test_tab.click()
        
    #     soup = self.get_soup()
    #     test_messages = len(soup.select('.nbmessage-border'))
    #     assert test_messages == messages_in_board[0]
        
    #     self.driver.save_screenshot('/opt/nbmessages/tests/acceptance/screenshots/admin-test-multi.png')
    
    def test_img_thumbnail_path_works(self):
        body = """# What is Lorem Ipsum
        
        Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.
        """

        input_name = 'My Name'
        self.create_message(self.board1, input_name, body, 'm1')
        
        
        self.proc.terminate()
        time.sleep(5)
        print(os.system('ls /srv/nbmessages/admin'))
        os.seteuid(0)
        self.launch_notebook_proc(['runuser', '-l', 'user1', '/opt/conda/bin/jupyter', 'notebook'])
        
        time.sleep(2)
        self.driver.get('http://127.0.0.1:8888')
        self.screenshot('whereami.png')
        self.navigate_to_mboard()
        
        print(self.get_soup())
        
        assert False
        
    
##### NEGATIVE TEST CODE
    # def test_add_message_with_same_id_fails(self):
    #     body1 = "# Hello\nThere"
    #     author1 = 'Name1'
    #     id_1 = 'm1'

    #     self.create_message(self.board1, author1, body1, id_1)
    #     self.driver.refresh()
        
    #     self.create_message(self.board1, author1, body1, id_1, close=False)
        
    #     soup = self.get_soup()
    #     self.driver.save_screenshot('/opt/nbmessages/tests/acceptance/screenshots/admin-mboard-same-id.png')

    #     assert soup.find(text='message_id = m1 already exist!')
