'''
Oliver Wilkins: 2020-02-06

This script sends a device's public IP address to a given email address.
'''

from CoreFunctions import Email, DatabaseConnection, get_ip
import json
import pandas as pd
from datetime import datetime


def get_email_pwd():
    # Get email details from private file
    email_file_path = '.private/email.json'

    with open(email_file_path, 'r') as json_file:
        data = json.loads(json_file.read())

    return data


def get_db_details():
    db_file_path = '.private/db.json'

    with open(db_file_path, 'r') as json_file:
        data = json.loads(json_file.read())

    return data


def check_ip_changed(db_ip, db_port, db_user, db_pwd, db_name, table_name, schema, ip):

    db = DatabaseConnection(
        host=db_ip,
        port=db_port,
        user=db_user,
        pwd=db_pwd,
        db=db_name,
    )

    df_ips = db.get_table_dataframe(table_name)

    if not df_ips.empty:
        # Get the IP address that was last used
        last_ip = df_ips.iloc[df_ips['time_detected'].idxmax()]['ip']

    if (ip not in df_ips['ip'].unique()) or (ip != last_ip):
        # if current IP is not in stored IPs OR
        # current IP does not equal the last IP used
        # write current IP

        df = pd.DataFrame(
            data=[[ip, str(datetime.now())]],
            columns=['ip', 'time_detected']
        )

        db.write_to_table(schema=schema, table_name=table_name, df=df)
        return True
    else:
        print('\nIP address already exists in table!')
        print('No action needed.')
        return False


def send_ip(email, pwd, ip):

    emailer = Email(
        self_email=email,
        password=pwd
    )

    body = 'Current Public IP Address: ' + ip

    print('\nSending public IP address to: ' + email + '...')

    emailer.send(
        to_email=email,
        subject='Current IP Address',
        body=body
    )

    print('Email sent!')


if __name__ == '__main__':

    print()
    print('-' * 10)
    print(f'Send IP Address Service started at : {datetime.now()}')
    print()

    email_pwd = get_email_pwd()
    db_details = get_db_details()
    ip = get_ip()

    ip_changed = check_ip_changed(
        db_ip=db_details['host'], db_port=db_details['port'],
        db_user=db_details['user'], db_pwd=db_details['password'],
        db_name=db_details['database'], schema=db_details['schema'],
        table_name=db_details['table'], ip=ip
    )

    if ip_changed:
        send_ip(
            email=email_pwd['email'],
            pwd=email_pwd['password'],
            ip=ip
        )
