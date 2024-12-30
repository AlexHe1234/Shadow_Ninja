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
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
from pyquery import PyQuery as pq

try:
    from .utils import *
except:
    from utils import *


class SearchSuNing(Search):
    def __init__(self,
                 max_retry: int = 10,
                 success_thresh: float = 0.5,  # if retrieved more than x of num_results
                 num_result: int = 3,
                 cookie_path: str = './tmp/suning_cookie.pkl',
                 num_history: int = 10,  # maximum history points
                 ):
        
        super().__init__(max_retry, success_thresh, num_result)
        
        self.pf = '苏宁'
        
        self.num_result = num_result
        self.cookie_path = cookie_path
        self.num_history = num_history
        
        os.makedirs(os.path.dirname(cookie_path), exist_ok=True)
        
        self.root_url = 'https://www.suning.com/'
        
        self.initialize()
        
    def initialize(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
        
        options = Options()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        # options.add_experimental_option("detach", True)
        
        self.driver = webdriver.Chrome(options=options)
        
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": """
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
            """
        })
        
        self.driver.get(self.root_url)
        self.load_cookies('suning.com')
        
        self.logged_in = False
        self.check_login()
        
        self.flag = True # additional avaiablility flag
        
    @property
    def available(self):
        return self.logged_in
        
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
        login_link = self.driver.find_element(By.CLASS_NAME, 'login')

        self.driver.execute_script("arguments[0].click();", login_link)
        time.sleep(2)     
        
        print('请手动进行登陆')
        
        try:
            _ = WebDriverWait(self.driver, 3000).until(
                EC.visibility_of_element_located((By.XPATH, "//*[text()='网页无障碍']"))
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
        
        self.quit_search()
        
        self.initialize()
        self.logged_in = True
                
    def _go(self, kws) -> Dict:
        
        kws = cat_strings([kw + ' ' for kw in kws])[:-1]

        driver = self.driver
        driver.get(self.root_url)
        
        # try the search box
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'searchKeywords'))
        )
        
        search_box.clear()
        search_box.send_keys(kws)
        search_box.send_keys(Keys.RETURN)

        time.sleep(2)
        # self.check_valid()

        # scrape! 
        element_list = [a for a in self.driver.find_elements(By.CSS_SELECTOR, "div.title-selling-point a")[:self.num_result]]
        # title-selling-point
        
        ret = []
    
        for i, element in tqdm(enumerate(element_list)):
            success, ret_one = self.scrape_one(element)
                                
            if success:
                print('Success')
                ret.append(ret_one)
            else:
                print('Failed')
                
            self.close_opened_windows()
            
            time.sleep(random.randint(1, 3))
               
        return {'results': ret}

    def scrape_one(self, element):
        success = False
        ret = {}
        
        time.sleep(0.5)
        element.click()
        time.sleep(0.5)
        
        # self.check_valid()
        
        try:
            
            # this is REALLY important
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[1])
                
            _ = WebDriverWait(self.driver, 2).until(
                EC.presence_of_element_located((By.ID, 'itemDisplayName'))
            )
            ret['name'] = self.driver.find_element(By.ID, 'itemDisplayName').text
            
            success = True
        except Exception as e:
            ret['name'] = ''
            print(f'{e}')
        
        try:
            # ret['price'] = self.driver.find_element(By.CLASS_NAME, 'arrival-price-txt').text
            
            main_price_container = self.driver.find_element(By.CSS_SELECTOR, "span.mainprice")
            integer_part = main_price_container.text.split('.')[0].strip()
            decimal_part = main_price_container.find_element(By.TAG_NAME, "span").text.strip()
            ret['price'] = integer_part[1:] + "." + decimal_part

            success = True
        except:
            ret['price'] = ''
            
        try:
            ret['image'] = self.driver.find_element(By.ID, 'bigImg').find_element(By.TAG_NAME,"img").get_attribute('src')
            success = True
        except:
            ret['image'] = 'https://media.istockphoto.com/id/1316134499/photo/a-concept-image-of-a-magnifying-glass-on-blue-background-with-a-word-example-zoom-inside-the.jpg?s=612x612&w=0&k=20&c=sZM5HlZvHFYnzjrhaStRpex43URlxg6wwJXff3BE9VA%3D'
            
        try:
            ret['platform'] = '苏宁'
            # success = True
        except:
            ret['platform'] = ''
        
        try:
            ret['class'] = self.driver.find_element(By.CLASS_NAME,"breadcrumb").text
            success = True
        except:
            ret['class'] = ''
            
        try:
            ret['size'] = self.driver.find_element(By.CLASS_NAME, 'tip-infor').text
            success = True
        except:
            ret['size'] = ''
            
        try:            
            ret['link'] = self.driver.current_url
            success = True
        except:
            # must have link
            success = False

        # breakpoint()
        print('Fetch done', success)

        if success:
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

        try:
            main_price_container = self.driver.find_element(By.CSS_SELECTOR, "span.mainprice")
            integer_part = main_price_container.text.split('.')[0].strip()
            decimal_part = main_price_container.find_element(By.TAG_NAME, "span").text.strip()
            return integer_part[1:] + "." + decimal_part
        except:
            return ''


if __name__ == '__main__':
    tb = SearchSuNing()
    ret = tb._go(['玩具儿童'])
    breakpoint()
