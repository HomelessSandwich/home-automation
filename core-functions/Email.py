import smtplib
from email.mime.text import MIMEText


class Email():
    def __init__(self, self_email, password):
        self.self_email = self_email
        self.password = password

    def __enter__(self):
        self.smtp = smtplib.SMTP('localhost', 1025)
        self.smtp.ehlo()
        self.smtp.starttls()
        self.smtp.ehlo()
        self.smtp.login(user=self.self_email, password=self.password)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.smtp.quit()

    def send(self, subject, body, to_email):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.self_email
        msg['To'] = to_email

        self.smtp.send_message(msg)

    def close_connection(self):
        self.smtp.quit()
