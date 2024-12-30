import os
import pickle
import random
from tqdm import tqdm
import requests
from bs4 import BeautifulSoup
import signal
from typing import Dict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

import time
from datetime import datetime
from pyquery import PyQuery as pq

try:
    from .utils import *
except:
    from utils import *


class SearchJingDong(Search):
    def __init__(
        self,
        max_retry: int = 10,
        success_thresh: float = 0.5,  # if retrieved more than x of num_results
        num_result: int = 3,
        cookie_path: str = './tmp/jingdong_cookie.pkl',
        num_history: int = 10,  # maximum history points
    ):
        
        super().__init__(max_retry, success_thresh, num_result)
        
        self.pf = '京东'
        
        self.num_result = num_result
        self.cookie_path = cookie_path
        self.num_history = num_history
        
        os.makedirs(os.path.dirname(cookie_path), exist_ok=True)
        
        self.root_url = 'https://www.jd.com/'
        
        self.initialize()

    def initialize(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
        
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        # options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option("useAutomationExtension", False)
        
        options.add_argument('--no-sandbox')  # Disable sandbox (important for Docker)
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited shared memory
        
        self.driver = webdriver.Chrome(options=options)
        
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        })
        
        try:
            self.driver.get(self.root_url)
        except:
            self.flag = False
            
        self.load_cookies('jd.com')
        
        self.logged_in = False
        self.check_login()
        
        self.flag = True # additional avaiablility flag
        
    @property
    def available(self):
        return self.logged_in and self.flag
    
    def quit_search(self):
        self.save_cookies()
        self.driver.quit()
        self.logged_in = False 

    def check_login(self):
                
        try:
            element = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((By.XPATH, "//*[text()='请登录']"))
            )
        except Exception as e:
            element = None  # login success

        if element is None:
            print('Logged in')
            self.logged_in = True
            return
        
        print('Not logged in, logging in')
        self.login()
        
    def login(self):
        # this process is hardly automatable, so please do it manually for ONCE
        # later login can be done autonomously through cookie
        
        # locating login link
        login_link = self.driver.find_element(By.CLASS_NAME, 'link-login')
        
        self.driver.execute_script("arguments[0].click();", login_link)
        
        print('请手动进行登陆')
        
        try:
            _ = WebDriverWait(self.driver, 3000).until(
                EC.visibility_of_element_located((By.XPATH, "//*[text()='切换至企业版']"))
            )
            try:
                self.driver.find_element(By.XPATH, "//*[text()='请登录']")
                print('登陆失败，请重试')
                exit()
            except:
                print('登陆成功')
        except:
            print('登陆超时，请重试')
            exit()
        
        self.save_cookies()
        self.logged_in = True
        
    def check_valid(self):
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[-1])
        
        # check for validate
        try:
            _ = WebDriverWait(self.driver, 0.1).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'verifyBtn'))
            )
            self.flag = False
            
            print('请验证后重新启动服务端继续使用')
            
            # self.driver.service.process.send_signal(signal.SIGTERM)
            # self.quit_search()
            time.sleep(100000)
        except:
            return
        # breakpoint()
        
    def _go(self, kws) -> Dict:
        
        kws = cat_strings([kw + ' ' for kw in kws])[:-1]

        driver = self.driver
        driver.get(self.root_url)
        
        # try the search box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'key'))
        )
        search_box.clear()
        search_box.send_keys(kws)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)
        self.check_valid()

        # scrape! the first try will alway fail
        # element_list = self.driver.find_elements(By.CLASS_NAME, 'gl-item')[:self.num_result + 1]
        
        element_list = self.driver.find_elements(By.CSS_SELECTOR, "div.p-name.p-name-type-2 > a")[:self.num_result + 1]

        ret = []
    
        for i, element in tqdm(enumerate(element_list)):
            success, ret_one = self.scrape_one(element)
                    
            if success:
                print('Success')
            else:
                print('Failed')
        
            if success and i > 0:
                ret.append(ret_one)
            
            self.close_opened_windows()
            
            time.sleep(random.randint(1, 3))
               
        return {'results': ret}
    
    @property
    def available(self):
        return self.logged_in and self.flag
    
    def scrape_one(self, element):
        success = False
        ret = {}
        
        time.sleep(0.5)
        element.click()
        time.sleep(0.5)
        
        self.check_valid()
        
        try:
            
            # this is REALLY important
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[1])
                
            _ = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'sku-name'))
            )
            
            ret['name'] = self.driver.find_element(By.CLASS_NAME, 'sku-name').text.split()[0]
            
            success = True
        except Exception as e:
            ret['name'] = ''
            print(f'{e}')
        
        try:
            ret['price'] = self.driver.find_element(By.CLASS_NAME, 'price').text
            success = True
        except:
            ret['price'] = ''
            
        try:
            ret['image'] = self.driver.find_element(By.ID, 'spec-img').get_attribute('src')
            success = True
        except:
            ret['image'] = 'https://media.istockphoto.com/id/1316134499/photo/a-concept-image-of-a-magnifying-glass-on-blue-background-with-a-word-example-zoom-inside-the.jpg?s=612x612&w=0&k=20&c=sZM5HlZvHFYnzjrhaStRpex43URlxg6wwJXff3BE9VA%3D'
            
        try:
            ret['platform'] = '京东'
            # success = True
        except:
            ret['platform'] = ''

        try:
            
            ret['class'] = cat_strings(self.driver.find_element(By.ID, "crumb-wrap").text.split('\n')[:-3])
            # ret['class'] = cat_strings([e.text + ' ' for e in self.driver.find_elements(By.CLASS_NAME, 'p-parameter-list')])
            success = True
        except:
            ret['class'] = ''
            
        try:
            
            def strip(x):
                xs = x.split()
                ret = ''
                for _xs in xs:
                    ret += _xs
                return ret
            
            ret['size'] = [strip(e.text) for e in self.driver.find_elements(By.CLASS_NAME, 'dd') if e.text != '']
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
    
    def check_price(self, link):

        self.check_login()
        self.close_opened_windows()
        
        self.driver.execute_script(f"window.open('{link}', '_blank');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        
        time.sleep(3)
        
        self.driver.close()
        
        time.sleep(2.5)
        self.driver.switch_to.window(self.driver.window_handles[0])
        
        time.sleep(2)
        self.driver.execute_script(f"window.open('{link}', '_blank');")
        
        time.sleep(2)
        # breakpoint()
        self.driver.switch_to.window(self.driver.window_handles[1])

        try:
            return self.driver.find_element(By.CLASS_NAME, 'price').text
        except:
            return ''


if __name__ == '__main__':
    tb = SearchJingDong()
    ret = tb.go(['保温杯 yeti'])
    breakpoint()
