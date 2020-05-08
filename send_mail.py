import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate


def send_mail(to, href):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.connect("smtp.gmail.com", 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.ehlo()

    textfile='templates/mail.html'
    with open(textfile) as fp:
        # Create MIMEMultipart message
        msg = MIMEMultipart()
        content = fp.read()
        content = content % ('http://mesenev.ru:1111/verify/' + href, 'http://mesenev.ru:1111/verify/' + href, 'http://mesenev.ru:1111/verify/' + href)
        #content = content % ('http://127.0.0.1:5000/verify/' + href, 'http://127.0.0.1:5000/verify/' + href, 'http://127.0.0.1:5000/verify/' + href)
        body = MIMEText(content, 'html')
        msg.attach(body)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = f'Verify your email'
    msg['From'] = 'verify-vidosos'
    msg["Date"] = formatdate(localtime=True)
    msg['To'] = to

    smtpObj.login('vidososverify@gmail.com', 'kek228lol')
    smtpObj.send_message(msg)
    smtpObj.quit()
