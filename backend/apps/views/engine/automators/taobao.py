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
import time
from pyquery import PyQuery as pq
from datetime import datetime

try:
    from .utils import *
except:
    from utils import *


class SearchTaobao(Search):
    def __init__(self,
                 max_retry: int = 10,
                 success_thresh: float = 0.5,  # if retrieved more than x of num_results
                 num_result: int = 5,
                 cookie_path: str = './tmp/taobao_cookie.pkl',
                 num_history: int = 10,  # maximum history points
                 ):
        super().__init__(max_retry, success_thresh, num_result)
        
        self.pf = '淘宝'
        
        self.num_result = num_result
        self.cookie_path = cookie_path
        self.num_history = num_history
        
        os.makedirs(os.path.dirname(cookie_path), exist_ok=True)
        
        self.root_url = 'https://www.taobao.com/'
        
        self.initialize()
        
    def initialize(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
        self.driver = webdriver.Chrome()
        
        self.driver.get(self.root_url)
        self.load_cookies('.taobao.com')
        
        self.logged_in = False
        self.check_login()
        
    @property
    def available(self):
        return self.logged_in
    
    def quit_search(self):
        self.save_cookies()
        self.driver.quit()
        self.logged_in = False
        
    def login(self):
        # this process is hardly automatable, so please do it manually for ONCE
        # later login can be done autonomously through cookie
        
        # locating login link
        login_link = self.driver.find_element(By.XPATH, "//*[text()='亲，请登录']")
        login_link.click()
        
        # input username and password
        # username_field = WebDriverWait(self.driver, 5).until(
        #     EC.visibility_of_element_located((By.ID, 'fm-login-id'))
        # )
        # username_field.send_keys(self.get_username())
        
        # password_field = WebDriverWait(self.driver, 5).until(
        #     EC.visibility_of_element_located((By.ID, 'fm-login-password'))
        # )
        # password_field.send_keys(self.get_passwd())
        
        print('请手动使用淘宝客户端二维码方式登陆')
        
        try:
            _ = WebDriverWait(self.driver, 3000).until(
                EC.visibility_of_element_located((By.XPATH, "//*[text()='网页无障碍']"))
            )
            try:
                self.driver.find_element(By.XPATH, "//*[text()='亲，请登录']")
                print('登陆失败，请重试')
                exit()
            except:
                print('登陆成功')
        except:
            print('登陆超时，请重试')
            exit()
        
        self.save_cookies()
        self.logged_in = True
        
    def check_login(self):
                
        try:
            element = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//*[text()='亲，请登录']"))
            )
        except Exception as e:
            element = None  # login success

        if element is None:
            print('Logged in')
            self.logged_in = True
            return
        
        print('Not logged in, logging in')
        self.login()
    
    def scrape_one(self, element):
        success = False
        ret = {}
        
        time.sleep(0.5)
        element.click()
        time.sleep(0.5)
        
        try:
            
            # this is REALLY important
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[1])
            
            _ = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'ItemTitle--UReZzEW5'))
            )
            
            ret['name'] = self.driver.find_element(By.CLASS_NAME, 'ItemTitle--UReZzEW5').text.split('\n')[0]
            
            success = True
        except Exception as e:
            ret['name'] = ''
            print(f'{e}')
        
        try:
            ret['price'] = self.driver.find_element(By.CLASS_NAME, 'text--fZ9NUhyQ').get_attribute('innerHTML')
            success = True
        except:
            ret['price'] = ''
            
        try:
            ret['image'] = self.driver.find_element(By.CLASS_NAME, 'mainPic--zxTtQs0P').get_attribute('src')
            success = True
        except:
            ret['image'] = 'https://media.istockphoto.com/id/1316134499/photo/a-concept-image-of-a-magnifying-glass-on-blue-background-with-a-word-example-zoom-inside-the.jpg?s=612x612&w=0&k=20&c=sZM5HlZvHFYnzjrhaStRpex43URlxg6wwJXff3BE9VA%3D'
            
        try:
            ret['platform'] = '淘宝'
            success = True
        except:
            ret['platform'] = ''
        
        try:
            ret['class'] = cat_strings([e.text for e in self.driver.find_elements(By.CLASS_NAME, 'infoItem--Z4hNxv8b')])
            success = True
        except:
            ret['class'] = ''
            
        try:
            ret['size'] = [e.text for e in self.driver.find_elements(By.CLASS_NAME, 'valueItem--GzWd2LsV  ')]
            success = True
        except:
            ret['size'] = ''
            
        try:            
            ret['link'] = self.driver.current_url
            success = True
        except:
            # must have link
            success = False

        print('Fetch done')

        if success:
            ret['history_price'] = self.get_history_price(self.driver.current_url)
            if (len(ret['history_price'])) == 0:
                current_datetime = datetime.now()
                ret['history_price'] = [[current_datetime.strftime('%Y-%m-%d %H:%M'), ret['price']]]
        else:
            ret['history_price'] = []
        
        self.close_opened_windows()
        
        return success, ret
    
    def _go(self, kws) -> Dict:
        
        kws = cat_strings([kw + ' ' for kw in kws])

        driver = self.driver
        driver.get(self.root_url)
        
        # try the search box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'q'))
        )
        search_box.clear()
        search_box.send_keys(kws)
        search_box.send_keys(Keys.RETURN)

        # wait for results to load
        time.sleep(2)

        # scrape!
        element_list = self.driver.find_elements(By.XPATH, "//*[contains(@id, 'item_id')]")[:self.num_result]
    
        ret = []
    
        for element in tqdm(element_list):
            success, ret_one = self.scrape_one(element)
        
            if success:
                print('Success')
            else:
                print('Failed')
        
            if success:
                ret.append(ret_one)
            
            self.close_opened_windows()
               
        return {'results': ret}
    
    def check_price(self, link):

        self.check_login()
        self.close_opened_windows()
        
        self.driver.execute_script(f"window.open('{link}', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[1])

        try:
            return self.driver.find_element(By.CLASS_NAME, 'text--fZ9NUhyQ').get_attribute('innerHTML')
        except:
            return ''


if __name__ == '__main__':
    tb = SearchTaobao()
    ret = tb.go(['玩具儿童'])
    breakpoint()
