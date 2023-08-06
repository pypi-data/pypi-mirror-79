# import unittest, os, subprocess, time, datetime, random, string, re

# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
# from nbmessages import APPLICATION_DATA_DIR

# from . import get_driver, BaseAcceptanceTester

# class TestSecurity(unittest.TestCase):
#     """Ensure other users cannot create messages"""
    
#     def setUp(self):
#         # runuser -l jovyan -c '/opt/conda/bin/jupyter notebook --ip 0.0.0.0 --NotebookApp.token=""'
#         os.system(f'mkdir -p {APPLICATION_DATA_DIR}/mboard')
#         os.system(f'mkdir -p {APPLICATION_DATA_DIR}/test')

#         os.seteuid(1000)
        
#         self.proc = subprocess.Popen(['jupyter', 'notebook', '--ip', '0.0.0.0', '--NotebookApp.token=""'])
#         time.sleep(2)
#         self.driver = get_driver()
#         self.driver.get('http://127.0.0.1:8888')

#     def tearDown(self):
#         os.seteuid(0)
#         self.proc.terminate()
#         os.system(f'rm -rf {APPLICATION_DATA_DIR}/mboard {APPLICATION_DATA_DIR}/test')

#     def get_soup(self):
#         source = self.driver.page_source
#         soup = BeautifulSoup(source, 'html.parser')
#         return soup

#     def test_non_owners_cannot_write(self):
#         board = 'test'
#         author = 'author'
#         body = 'test'
#         m_id = 'm1'
        
#         admin_tab = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'nbmessages (Admin)')))
#         admin_tab.click()
        
#         # make sure we select a message board first
#         select_board = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'select-message-board')))

#         for option in select_board.find_elements_by_tag_name('option'):
#             if option.text == board:
#                 option.click()
#                 break

#         messages = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Messages')))
#         messages.click()

#         # fill in the name
#         name = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'author')))
#         name.send_keys(author)

#         # fill in the message ID
#         message_id_el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'message_id')))
#         message_id_el.send_keys(m_id)

#         # fill in the body        
#         message_body_el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'message_body')))
#         message_body_el.send_keys(body)            
            

#         # submit, save, and close
#         # (By.XPATH, '//*[@id="nbmessage-admin"]/button')
#         submit_el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nbmessage-admin>button')))
#         submit_el.click()

#         time.sleep(1)

#         # (By.XPATH, '//*[@id="save-message"]')
#         save_el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'save-message')))
#         save_el.click()

#         time.sleep(1)
#         self.driver.save_screenshot('/opt/nbmessages/tests/acceptance/screenshots/security.png')
        
#         soup = self.get_soup()

#         res = soup.findAll(text='You dont have permissions to create messages for message board = test')
        
#         assert len(res) > 1
