import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import email
import imaplib


class EmailService:
    def __init__(
        self,
        account: str = 'alexhe_bs_proj@163.com',  # an anonymous email account I registered for this project
        password: str = 'KAv3musMFbrg8Jfr',
    ):
        
        # use email stack, which provides much more function than this task
        # I wrote it for another project, but anyway
        self.email_stack = EmailStack(account=account, password=password)
        
    def send(self, recipient, subject, body):
        self.email_stack.__send__(subject=subject, body=body, recipient=recipient)
        

# Utilize an email account as multiple 'online' stacks distinguished by stack_id
class EmailStack:
    def __init__(self,
                 account: str,  # NOTE: these have to be the SAME to access the SAME stack
                 password: str,
                 stack_id: int = 0,
                 ):
        self.account = account
        self.password = password
        self.stack_id = stack_id
        self.smtp_addr = 'smtp.' + self.account.split('@')[-1]
        self.imap_addr = 'imap.' + self.account.split('@')[-1]
        
        try:
            self.smtp_server = smtplib.SMTP()
            # self.smtp_server.starttls()
            self.smtp_server.connect(self.smtp_addr, 25)
            self.smtp_server.login(self.account, self.password)
        except:
            raise RuntimeError('SMTP login failed')
        
        try:
            self.imap_server = imaplib.IMAP4_SSL(self.imap_addr, 993)
            self.imap_server.login(self.account, self.password)
            self.imap_server.select('inbox')
        except:
            raise RuntimeError('IMAP login failed')
        
    def push(self, msg: str):
        self.__send__(str(self.stack_id), msg)

    def __send__(self, subject: str, body: str, recipient: str = None):
        message = MIMEMultipart()
        
        to_account = self.account if recipient is None else recipient
        message['From'] = to_account
        message['To'] = self.account
        message['Subject'] = subject
        
        message.attach(MIMEText(body, 'plain'))
        text = message.as_string()
        try:
            self.smtp_server.sendmail(self.account, to_account, text)
        except:
            raise RuntimeError('Email account is not accessible')

    # return newest mail content with certain stack_id
    def top(self):
        result, data = self.imap_server.search(None, 'ALL')
        assert result == 'OK', 'IMAP search inbox failed'
        
        for num in reversed(data[0].split()):
            result, data = self.imap_server.fetch(num, '(RFC822)')
            assert result == 'OK', 'IMAP fetch email failed'
            
            raw_email = data[0][1]
            msg = email.message_from_bytes(raw_email)
            
            subject = msg['Subject']
            
            if subject != str(self.stack_id): continue
                    
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode()
                        break
            else:
                body = msg.get_payload(decode=True).decode()
                
            return body

        return None

    def close(self):
        self.imap_server.logout()


if __name__ == '__main__':
    
    service = EmailService()
    service.send('alexhe2000@zju.edu.cn', '[test]', 'hey there, if you receive this, it means the code works fine')
    