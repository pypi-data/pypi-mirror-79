# import time, datetime, random, string

# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
# from nbmessages import APPLICATION_DATA_DIR

# from . import get_driver, BaseAcceptanceTester

# class TestMessageDeleteSystem(BaseAcceptanceTester):
#     def test_delete(self):
#         try:
#             self.m_id = 'm_id'
#             self.create_message('mboard', 'auth1', 'my body', self.m_id, True, False)
#             self.navigate_to_mboard()
            
#             # navigate back to messages
#             self.navigate_to_admin_tab()
#             self.select_board('mboard')
            
#             messages = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Messages')))
#             messages.click()

#             select_board = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'nbmessage-operation')))

#             for option in select_board.find_elements_by_tag_name('option'):
#                 if option.text == 'Delete':
#                     option.click()
#                     break
                
#             delete_select = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'delete-message')))
#             for option in delete_select.find_elements_by_tag_name('option'):
#                 if option.text == self.m_id:
#                     option.click()
#                     break
            
#             #//*[@id="nbmessage-admin-delete"]/button
#             submit = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
#             submit.click()
            
#             time.sleep(2)
#             #//*[@id="save-message"]
#             save = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="save-message"]')))
#             save.click()
            
#             time.sleep(2)
#             close = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'close-modal')))
#             close.click()
            
#             time.sleep(2)
            
#             self.navigate_to_mboard()
            
#             soup = self.get_soup()
#             res = soup.find(text='No messages yet')
#             assert len(res) >= 1

#         except Exception as e:
#             self.screenshot('delete.png')
#             raise e