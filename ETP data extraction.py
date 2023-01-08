# Created By  : Zulmi Yahya
# Created Date: 16/02/2022
# version ='1.0'
""" Clean the Swab Status Script into OOP"""

import csv
import pandas as pd
import smtplib
import json

from pyhive import presto
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

class EmailSender:
    
    def __init__(self, filename):
        self._filename = filename
        
    def get_filename(self):
        return self._filename
    
    def set_filename(self, filename):
        self._filename = filename
    
    def send_email(self):
        try:
            with open('config.json', 'r') as jsonfile:
                data = json.load(jsonfile)

            for receiver in data['mail_to']:

                mimemsg = MIMEMultipart()
                mimemsg['From'] = data['mail_from']
                mimemsg['To'] = receiver
                mimemsg['Subject'] = data['mail_subject']
                mimemsg.attach(MIMEText(data['mail_body'], 'plain'))

                with open(EmailSender.get_filename(self), "rb") as attachment:
                    mimefile = MIMEBase('application', 'octet-stream')
                    mimefile.set_payload((attachment).read())
                    encoders.encode_base64(mimefile)
                    mimefile.add_header('Content-Disposition', "attachment; filename= %s" % EmailSender.get_filename(self))
                    mimemsg.attach(mimefile)

                connection = smtplib.SMTP(host='smtp.office365.com', port=587)
                connection.starttls()
                connection.login(data['username'], data['password'])
                connection.send_message(mimemsg)
                connection.quit()
            print('Successfully sent.')
        except FileNotFoundError as e:
            print(f'Message was not sent\n{e}')
                

class RetrieveSwab:
    
    def runQuery(self):  
        try:
            currentdatetime = datetime.strftime(datetime.now(), '%Y%m%d-%H%M')
            
            cursor = presto.connect(host="hadoop2",port=8443, username="zulmi").cursor()
            cursor.execute('''
            SELECT * FROM(
            SELECT''')
            print("Data is extracting...")
        except Exception as e:
            print("Fail: ", e)
        else:
            rows = [i for i in cursor.fetchall()]
            with open('result/%s-swab_status.csv' % (currentdatetime), 'w') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow([i[0] for i in cursor.description])
                for row in rows:
                    writer.writerow(row)
            print('Extraction complete, total rows:', len(rows))

        finally:
            df = pd.read_csv(r'/home/zulmi.yahya/result/%s-swab_status.csv' % (currentdatetime))
            df.to_parquet('swab_status.parquet')
            print('Data has been converted into parquet.')

if __name__ == '__main__':
    swab = RetrieveSwab()
    swab.runQuery()
    email = EmailSender('swab_status.parquet')
    email.send_email()