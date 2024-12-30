import time
import random
import pickle
from typing import Dict
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def cat_strings(strings):
    return ''.join(s.replace('\n', '') for s in strings)


class Search:
    def __init__(self, max_retry, success_thresh, num_result):
        super().__init__()
        self.max_retry = max_retry
        self.success_thresh = success_thresh
        self.num_result = num_result
        
        self.num_success = int(self.success_thresh * self.num_result)
        
    def assert_object(self):
        if type(self) is Search:
            raise NotImplementedError('Do not call from a Search object, using child objects instead')
        
    def save_cookies(self):
        self.assert_object()
        with open(self.cookie_path, "wb") as cookie_file:
            pickle.dump(self.driver.get_cookies(), cookie_file)

    def load_cookies(self, kw):
        self.assert_object()
        try:
            with open(self.cookie_path, "rb") as cookie_file:
                cookies = pickle.load(cookie_file)
                for cookie in cookies:
                    if kw not in cookie['domain']: continue
                    self.driver.add_cookie(cookie)
            
            self.driver.refresh()
            time.sleep(1)  # wait for cookie to load
            
            print("Cookies loaded successfully.")
        except Exception as e:
            print(f"No cookies loaded. {e}")
        
    def go(self, kws) -> Dict:
        self.assert_object()
        
        for i in range(self.max_retry):
            try:
                ret = self._go(kws)
                if len(ret['results']) < self.num_success:
                    raise Exception()
                else:
                    return ret
            except Exception as e:
                print(f"Attempt {i + 1} failed: {e}. Retrying...")
                self.initialize()
                time.sleep(1)

        print('Failed, returning empty results')
        return {'results': []}

    def close_opened_windows(self):
        time.sleep(0.5)
        
        try:
            driver = self.driver
            
            if len(driver.window_handles) <= 1: return

            while len(driver.window_handles) > 1:
                driver.switch_to.window(driver.window_handles[1])
                driver.close()
                
            driver.switch_to.window(driver.window_handles[0])
        except:
            return
        
    def random_scroll(self, max_scrolls=5, scroll_range=[-500, 500]):
        driver = self.driver
        for _ in range(max_scrolls):
            scroll_amount = random.randint(*scroll_range)
            driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
            time.sleep(random.uniform(0.5, 2.0))
        driver.execute_script("window.scrollTo(0, 0);")
        
    def get_history_price(self, url):
        try:
            url_0, url_1 = url.split('.com')
            
            url_new = url_0 + 'vvv.com' + url_1
            self.driver.execute_script(f"window.open('{url_new}');")
            
            windows = self.driver.window_handles
            self.driver.switch_to.window(windows[-1])
            
            try:
                _ = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.TAG_NAME, 'li'))
                )
            except Exception as e:
                print('Get history failed:', e)
            
            ret = []
            list_element = self.driver.find_element(By.ID, 'youhuiUl').get_attribute('outerHTML')
            
            elements = list_element.split('li')

            for e in elements:
                if 'time' not in e or '优惠后' not in e: continue
                
                e_time = e.split('time">')[-1]
                t = e_time[:len('2024-12-26 00:09')]
                
                e_price = e_time.split('优惠后')[-1].split('元')[0]
                p = e_price
                
                ret.append([t, p])
                
                if len(ret) >= self.num_history: break
                
            return ret

        except Exception as e:
            print('get history failed because ', e)    
            return []
