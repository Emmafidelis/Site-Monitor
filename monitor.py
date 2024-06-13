import smtplib
import requests
import config
from linode_api4 import LinodeClient, Instance

EMAIL_ADDRESS = config.EMAIL_USER
EMAIL_PASSWORD = config.EMAIL_PASS
LINODE_TOKEN = config.LINODE_KEY

def notify_user():
  with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    subject = 'Your site is down'
    body = 'Make sure the server restarted and it is back up'
    msg = f'subject: {subject}\n\n{body}'

    smtp.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg)

def reboot_server():
  client = LinodeClient(LINODE_TOKEN)
  my_server = client.load(Instance, 376715)
  my_server.reboot()

try:
  r = requests.get('https://coreyms.com', timeout=5)

  if r.status_code != 200:
    notify_user()
    reboot_server()
except Exception as e:
  notify_user()
  reboot_server()

  