import time
import argparse
from email_utils import EmailService

from automators import SearchJingDong, SearchSuNing, SearchTaobao
from automators.utils import Search


class Notification:
    def __init__(self, 
                 price: float,
                 platform: str,
                 link: str,
                 email: str,
                 user: str,
                 max_retry_per_day: int = 5):
        self.email_service = EmailService() # valid until 2025-02-28
        
        self.price = price
        self.platform = platform
        self.link = link
        self.email = email
        self.user = user
        
        self.max_retry = max_retry_per_day
        self.has_run = False
        
        self.platform: Search

        if platform == '淘宝':
            self.platform = SearchTaobao()
            print('Notification ready')
        elif platform == '苏宁':
            self.platform = SearchSuNing()
            print('Notification ready')
        elif platform == '京东':
            self.platform = SearchJingDong()
            print('Notification ready')
        else:
            print(f'platform {platform} not found')
            exit(1)

    def notify(self):
        
        email = self.email
        user = self.user
        item_link = self.link
        
        msg = f'亲爱的「{user}」你好，你订阅的商品降价了，快去看看吧。商品链接: {item_link}'
        
        try:
            self.email_service.send(email, '[ShopSmart] 降价提醒', msg)
            print(f'邮件成功发送至{email}')
            
        except Exception as e:
            print(f'邮件发送失败，原因是：{e}')

        self.has_run = True

    def check(self):
        
        price = self.platform.check_price(self.link)

        if price == '':
            return
        
        print(f'og price: {self.price}; current price {float(price)}')
    
        if float(price) < self.price:
        # if True:
            self.notify()
    
    def quit(self):
        print('Quitting')
        self.platform.quit_search()
        
    def run(self):
        
        while True:

            try:
                self.check()
            except Exception as e:
                print(f'Check price failed because {e}')
                
            if self.has_run:
                self.quit()
                return
            
            time.sleep(86400 / self.max_retry)


def main():
    parser = argparse.ArgumentParser(description="price, link, email, and platform inputs.")

    parser.add_argument("--price", type=float, help="Specify the price (e.g., 178.50).")
    parser.add_argument("--link", type=str, help="Provide the link (URL).")
    parser.add_argument("--email", type=str, help="Provide the email address.")
    parser.add_argument("--username", type=str, help='')
    parser.add_argument("--platform", type=str, help="Specify the platform (e.g., website name).")
    args = parser.parse_args()

    print('Subscribtion script starts')

    print(f"Price: {args.price}")
    print(f"Link: {args.link}")
    print(f"Email: {args.email}")
    print(f"Platform: {args.platform}")
    print(f"Username: {args.username}")
    
    notification = Notification(price=args.price, platform=args.platform, link=args.link, email=args.email, user=args.username)
    notification.run()
    
    print('Ended')


if __name__ == "__main__":
    main()
