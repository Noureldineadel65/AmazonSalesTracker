import sys
import requests
from bs4 import BeautifulSoup as bs
import logging
import smtplib
logging.basicConfig(level=logging.DEBUG, format=(
    ' %(asctime)s - %(levelname)s - %(message)s'))

logging.debug('Start of the Program')
if (len(sys.argv) > 2):
    email = sys.argv[1]
    password = sys.argv[2]
else:
    raise Exception(
        'You need to provide an email, and password respectively')
link = input("Enter the link to your amazon product")
priceyoulike = int(
    input('Enter the price you would like for us to notify you at'))


def sendMail(item, priceofitem, link, company):
    print('Connecting to server....')
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email, password)
    subject = f"The price of {item}"
    body = f"Check the {company} link: {link}"
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(email,
                    email, msg)
    print(f'Email has been sent to you at {email}. Check it out!')


url = link

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

requestPage = requests.get(url, headers=headers)
soup = bs(requestPage.content, 'lxml')
title = soup.find(id='productTitle').get_text().strip()
price = soup.find(id='priceblock_ourprice').get_text()
price = int(price.split('.')[0][1:]) + 1
if price < priceyoulike:
    sendMail(title, price, url, 'amazon')
