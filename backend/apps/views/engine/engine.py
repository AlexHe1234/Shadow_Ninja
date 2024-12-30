import os
import subprocess
from typing import Dict, List

from .email_utils import EmailService
from .language_utils import WordMaster
from .automators import SearchTaobao, SearchJingDong, SearchSuNing


class SearchEngine:
    def __init__(
        self,
        mp: bool = False,  # default to multiprocess search for faster response
        init_num_result: int = 3, # if not provided otherwise use this
        word_master_cfg: Dict = {},
        use: List = ['tb', 'jd', 'sn'],
    ):
        super().__init__()

        print('Engine initializing')
        
        self.default_num_result = init_num_result
        self.use_mp = mp
        
        self.wm = WordMaster(**word_master_cfg)
                
        self.platforms = []
        for pf in use:
            
            # add auto matching for platforms by enforcing "name" field for every platform class
            if pf == 'tb':
                self.platforms.append(SearchTaobao(num_result=init_num_result))
                print(f'Added platform {self.platforms[-1].pf}')
            
            if pf == 'jd':
                self.platforms.append(SearchJingDong(num_result=init_num_result))
                print(f'Added platform {self.platforms[-1].pf}')
                
            if pf == 'sn':
                self.platforms.append(SearchSuNing(num_result=init_num_result))
                print(f'Added platform {self.platforms[-1].pf}')
        
        print('Engine is ready')
        
    def segment(self, word) -> List[str]:
        return self.wm.segment_word(word)

    def launch_search(self, kw: List[str]):
        print(f'Launching search on {len(self.platforms)} platforms')
        
        if self.use_mp:
            return self.launch_search_parallel(kw)
        else:
            return self.launch_search_sequential(kw)    
        
    def subscribe(self, price, link, user, email, platform):
        
        try:

            cmd = [
                'python3',  # Or 'python' depending on your environment
                os.path.join(os.path.dirname(__file__), 'notification.py'),
                '--price', f'{price}',
                '--link', f'{link}',
                '--email', f'{email}',
                '--username', f'{user}',
                '--platform', f'{platform}',
            ]
            
            print(cmd)
            
            subprocess.Popen(cmd)
            
            return True
        
        except Exception as e:
            
            print(f'Subscription failed, reason: {e}')
            return False

    # TODO:
    def launch_search_parallel(self, kw: List[str]):
        raise NotImplementedError()
        
    def launch_search_sequential(self, kw: List[str]):
        ret = []
        
        for pf in self.platforms:
            
            if not pf.available:
                print(f'{pf.pf} 不可用，请人工查看处理')
                continue
            
            try:
                result = pf.go(kw)
                ret.append(result['results'])
            except: # ? add retry mechanism
                pass

        return ret
        
    def process_results(self, results: Dict):

        num_platform = len(self.platforms)
        
        ret = {'results': []}
        for i in range(num_platform):
            
            result_pf = results[i] # already the results dict list
            if len(result_pf) < 1: continue
            
            ret['results'] += result_pf
        
        return ret
    
    # ! deprecated, email service is provided by separate module
    def notify(self, email: str, user: str, item_name: str, item_link: str):
        
        msg = f'亲爱的「{user}」你好，你订阅的商品{item_name}降价了，快去看看吧。商品链接: {item_link}'
        
        try:
            self.email_service.send(email, '[ShopSmart.] 降价提醒', msg)
            print(f'邮件成功发送至{email}')
        except Exception as e:
            print(f'邮件发送失败，原因是{e}')
    
    def search(self, query: str):
        
        keywords = self.segment(query)
        if len(keywords) == 0:
            return {'results': []}
        
        results = self.launch_search(keywords)
        results = self.process_results(results)
        
        return results
