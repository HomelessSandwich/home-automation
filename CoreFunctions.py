import smtplib
import requests
import pandas as pd
from sqlalchemy import create_engine
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


class DatabaseConnection:
    def __init__(self, host, port, user, pwd, db):
        try:
            print(f"\nAttemping to connect to server: {user}@{host}:{port}/{db}")
            conn_str = f'postgresql://{user}:{pwd}@{host}:{port}/{db}'
            self.engine = create_engine(conn_str)

        except Exception as e:
            print("Cannot connect to the database!")
            print(e)
            print("\nDatabase connection closed.")
        else:
            print("Connection successful!")

    def get_table_dataframe(self, table_name):
        """
        Puts a table from a database into a pandas data frame.
        Inputs:
            table_name (str): name of the table from the database
        Returns: pandas dataframe
        """
        print(f"\nAttempting to read table: {table_name}")

        try:
            # Read table from database
            # fillna to avoid casting issues of integer cols that have NULLS
            df = pd.read_sql(f"SELECT * FROM {table_name}", con=self.engine)
            df = df.where((pd.notnull(df)), None)
        except Exception as e:
            print("Could not get table and put into pandas dataframe!")
            print(e + "\n")
            # Return empty dataframe
            df = pd.DataFrame()
        else:
            print(f"Reading successful: {table_name}")
        finally:
            return df

    def execute(self, cmd=''):
        '''
        Executes an SQL command.

        cmd (str): The SQL command to be executed.
        '''

        result = self.engine.execute(cmd)
        return result

    def write_to_table(self, table_name, schema, df):
        '''
        Writes Pandas dataframe to a table.

        table_name (str): The name of the table to be written to.
        schema (str): The name of the schema, containing the table to be written to.
        df (pandas.DataFrame): The dataframe containing the data to write from.
        '''

        print('\nAttempting to write to:')
        print(f'\tSchema: {schema} | Table: {table_name}')

        try:
            df.to_sql(
                name=table_name, schema=schema, con=self.engine,
                if_exists='append', index=False
            )
        except Exception as e:
            print("Could not write dataframe to table!")
            print(e + "\n")
        else:
            print('Sucessful to write to:')
            print(f'\tSchema: {schema} | Table: {table_name}')


def get_ip():
    # Gets current public IP address

    print('Requesting public ip address...')
    r = requests.get('http://ip.me')
    ip = r.text.strip()

    print('IP Address: ' + ip + '\n')

    return ip
