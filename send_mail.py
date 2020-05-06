import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText

def send_mail(to, href):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.connect("smtp.gmail.com", 587)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.ehlo()

    textfile='templates/mail.html'
    with open(textfile) as fp:
        # Create a text/plain message
        msg = EmailMessage()
        content = fp.read()
        content = content % ('http://mesenev.ru:1111/verify/' + href, 'http://mesenev.ru:1111/verify/' + href, 'http://127.0.0.1:5000/verify/' + href)
        body = MIMEText(content, 'html')
        msg.set_content(body)

    # me == the sender's email address
    # you == the recipient's email address
    msg['Subject'] = f'Verify your email'
    msg['From'] = 'verify-vidosos'
    msg['To'] = to

    smtpObj.login('vidososverify@gmail.com', 'kek228lol')
    smtpObj.send_message(msg)
    smtpObj.quit()
