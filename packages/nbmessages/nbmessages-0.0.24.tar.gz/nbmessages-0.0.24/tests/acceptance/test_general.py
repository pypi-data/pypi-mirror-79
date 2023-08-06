# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from bs4 import BeautifulSoup
# from nbmessages import APPLICATION_DATA_DIR

# from . import get_driver, BaseAcceptanceTester

# class TestGeneralFeatures(BaseAcceptanceTester):
#     def test_host(self):
#         self.driver.get('http://127.0.0.1:8888')
#         assert self.driver.title == 'Home Page - Select or create a notebook'
    
#     def test_plugins_viewable(self):
#         # tabs must exist
#         admin_tab = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'nbmessages-admin')))
#         assert True

#     def test_global_can_select_multiple(self):
#         admin_tab = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.LINK_TEXT, 'nbmessages (Admin)')))
#         admin_tab.click()

#         select_board = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'select-message-board')))

#         found_test = False
#         found_mboard = False
#         for option in select_board.find_elements_by_tag_name('option'):
#             if option.text == 'test':
#                 option.click()
#                 found_test = True
#             elif option.text == 'mboard':
#                 found_mboard = True

#         assert found_test
#         assert found_mboard