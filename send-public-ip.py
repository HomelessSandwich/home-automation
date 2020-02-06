'''
Oliver Wilkins: 2020-02-06

This script sends a device's public IP address to a given email address.
'''

from CoreFunctions.Email import Email
import json
import requests


def get_email_pwd():
    # Get email details from private file
    email_file_path = '.private/email.json'

    with open(email_file_path, 'r') as json_file:
        data = json.loads(json_file.read())

    return data


def get_ip():
    # Gets current public IP address

    print('Requesting public ip address...')
    r = requests.get('http://ip.me')
    ip = r.text.strip()

    print('IP Address: ' + ip + '\n')

    return ip


def send_ip(email, pwd, ip):

    emailer = Email(
        self_email=email,
        password=pwd
    )

    body = 'Current Public IP Address: ' + ip

    print('Sending public IP address to: ' + email + '...')

    emailer.send(
        to_email=email,
        subject='Current IP Address',
        body=body
    )

    print('Email sent!')


if __name__ == '__main__':
    email_pwd = get_email_pwd()
    ip = get_ip()

    send_ip(
        email=email_pwd['email'],
        pwd=email_pwd['password'],
        ip=ip
    )
