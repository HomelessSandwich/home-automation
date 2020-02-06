import smtplib
import requests
from email.mime.text import MIMEText


class Email():
    def __init__(self, self_email, password):
        self.self_email = self_email
        self.password = password

        self.smtp = smtplib.SMTP('smtp.gmail.com:587')
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.ehlo()
        self.smtp.login(user=self.self_email, password=self.password)

    def send(self, subject, body, to_email):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.self_email
        msg['To'] = to_email

        self.smtp.send_message(msg)

    def close_connection(self):
        self.smtp.quit()


def get_ip():
    # Gets current public IP address

    print('Requesting public ip address...')
    r = requests.get('http://ip.me')
    ip = r.text.strip()

    print('IP Address: ' + ip + '\n')

    return ip
