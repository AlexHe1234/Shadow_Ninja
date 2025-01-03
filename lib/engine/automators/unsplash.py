import os
import pickle
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
from typing import Dict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains

import time
from pyquery import PyQuery as pq
from datetime import datetime

try:
    from .utils import *
except:
    from utils import *
    
    
class Unsplash(Search):
    def __init__(
        self,
        max_retry: int = 10,
        success_thresh: float = 0.5,  # if retrieved more than x of num_results
        num_result: int = 5,
        cookie_path: str = './tmp/unsplash_cookie.pkl',
        num_history: int = 10,  # maximum history points
    ):
        super().__init__(max_retry, success_thresh, num_result)
        
        self.pf = 'unsplash'
        
        self.num_result = num_result
        self.cookie_path = cookie_path
        self.num_history = num_history
        
        os.makedirs(os.path.dirname(cookie_path), exist_ok=True)
        
        self.root_url = 'https://unsplash.com/'
        
        self.initialize()
        
    def initialize(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
        
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(options=options)
        
        self.driver.get(self.root_url)
        self.load_cookies('unsplash.com')
        
        self.logged_in = False
        # self.check_login()

    def run(self, search_word, num_result):

        if len(self.driver.window_handles) > 1:
            self.initialize()
        
        self.driver.switch_to.window(self.driver.window_handles[-1])
        
        search_box = self.driver.find_element(By.CLASS_NAME, 'N3ti0')
        search_box.click()
        time.sleep(0.2)   
        text_box = self.driver.find_element(By.CLASS_NAME, 'DevoO')
        text_box.clear()
        time.sleep(0.2)
        text_box.send_keys(search_word)
        time.sleep(0.2)
        text_box.send_keys(Keys.RETURN)
        
        time.sleep(2)
        
        progress_bar = tqdm(total=num_result, desc="Progress", unit="step")
        
        try:
            download_links = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="non-sponsored-photo-download-button"]')
            saved_links = []
            
            while len(download_links) < num_result:
                
                try:
                    
                    for i in range(0, 3000000, 10):  
                        self.driver.execute_script(f"window.scrollBy(0, {i});")
                        time.sleep(0.02)
                    
                        try:
                            load_button = WebDriverWait(self.driver, 0.01).until(
                                EC.presence_of_element_located((By.XPATH, '//button[text()="Load more"]'))
                            )

                            ActionChains(self.driver).move_to_element(load_button).perform()

                            load_button.click()
                        except:
                            pass
                    
                        download_links = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="non-sponsored-photo-download-button"]')
                        for link in download_links:
                            
                            href = link.get_attribute('href')
                            
                            if href is not None and href not in saved_links:
                                saved_links.append(href)
                                
                                progress_bar.update()
                
                        if len(download_links) > num_result:
                            break
                
                except Exception as e:
                    
                    print(f'Unsplash find load more button failed: {e}')
                    
                    break # there are no more images
            
            # download_links = self.driver.find_elements(By.CSS_SELECTOR, '[data-testid="non-sponsored-photo-download-button"]')
            
            ret = saved_links
            
        except Exception as e:
            print(f'Unsplash failed: {e}')
            ret = []
            
        return ret

    @property
    def available(self):
        return True
        