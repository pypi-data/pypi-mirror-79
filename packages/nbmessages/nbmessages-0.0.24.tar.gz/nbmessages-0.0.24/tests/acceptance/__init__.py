import subprocess, unittest, os, time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from nbmessages import APPLICATION_DATA_DIR

def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver', options=chrome_options)

    return driver

class BaseAcceptanceTester(unittest.TestCase):
    def setUp(self):
        
        os.system(f'mkdir -p {APPLICATION_DATA_DIR}/mboard')
        os.system(f'mkdir -p {APPLICATION_DATA_DIR}/test')
        
        os.system(f'chown -R 1000:1000 {APPLICATION_DATA_DIR}')
        os.system(f'chmod -R 0755 {APPLICATION_DATA_DIR}')
        os.seteuid(1000)
        self.launch_notebook_proc()
        self.driver = get_driver()
        
        # FIXME make this better to wait for the server to start
        time.sleep(2)
        self.driver.get('http://127.0.0.1:8888')
        
        self.board1 = 'mboard'
        self.board2 = 'test'
        
        os.system(f'mkdir -p {APPLICATION_DATA_DIR}/mboard')
        os.system(f'mkdir -p {APPLICATION_DATA_DIR}/test')

    def tearDown(self):
        os.seteuid(0)
        self.proc.terminate()
        os.system(f'rm -rf {APPLICATION_DATA_DIR}/mboard {APPLICATION_DATA_DIR}/test')
    
    def launch_notebook_proc(self, default=['jupyter', 'notebook', '--ip', '0.0.0.0', '--NotebookApp.token=""']):
        self.proc = subprocess.Popen(default)
    
##### HELPER FUNCTIONS
    def navigate_to_admin_tab(self):
        admin_tab = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'nbmessages (Admin)')))
        admin_tab.click()
            
    def select_board(self, board):
        select_board = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'select-message-board')))

        for option in select_board.find_elements_by_tag_name('option'):
            if option.text == board:
                option.click()
                break

    def create_message(self, board, author, body, m_id, close=True, add_notification=False, expiration_date='06/10/2020'):
        try:
            self.navigate_to_admin_tab()
            
            # make sure we select a message board first
            self.select_board(board)

            messages = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Messages')))
            messages.click()

            # fill in the name
            name = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'author')))
            name.send_keys(author)

            # fill in the message ID
            message_id_el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'message_id')))
            message_id_el.send_keys(m_id)

            # fill in the body        
            message_body_el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'message_body')))
            message_body_el.send_keys(body)
            
            if add_notification:
                notification_check = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'set_notification')))
                notification_check.click()
                
                expiration = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.NAME, 'expiration_date')))
                expiration.send_keys(expiration_date)
                
            # submit, save, and close
            # (By.XPATH, '//*[@id="nbmessage-admin"]/button')
            submit_el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#nbmessage-admin>button')))
            submit_el.click()

            time.sleep(1)

            # (By.XPATH, '//*[@id="save-message"]')
            save_el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.ID, 'save-message')))
            save_el.click()

            time.sleep(1)
            
            if close:
                # (By.XPATH, "(//button[@id='close-modal'])[3]")
                close_el = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.ID, 'close-modal')))
                close_el.click()
                time.sleep(1)
        except:
            self.driver.save_screenshot('/opt/nbmessages/tests/acceptance/screenshots/error.png')

    def get_soup(self):
        source = self.driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        return soup

    def navigate_to_mboard(self):
        # check announcements tab
        announcements = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, 'Announcements')))
        announcements.click()
        
        # check that the mboard tab has the message
        mboard_tab = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.LINK_TEXT, 'mboard')))
        mboard_tab.click()
        mboard_tab.click()
        
        time.sleep(1)
        
        soup = self.get_soup()
        
    def screenshot(self, name):
        self.driver.save_screenshot(f'/opt/nbmessages/tests/acceptance/screenshots/{name}')