
import smtplib
from email.mime.text import MIMEText


def send_email(sender, receiver, SMTP_server, message, request_id):
    '''

    :param sender:
    :param receiver:
    :param SMTP_server:
    :param message:
    :param request_id:
    :return:
    '''
    msg = MIMEText(message)
    msg['Subject'] = 'HIV Molecular Dating Request ID %s' % request_id
    msg['From'] = sender
    msg['To'] = receiver
    s = smtplib.SMTP("smtp.gmail.com",587)
    s.ehlo()
    s.starttls()
    s.login('shivankurkapoor3192@gmail.com', '')
    s.sendmail(sender, [receiver], msg.as_string())
    s.quit()

send_email('shivankurkapoor3192@gmail.com','kapoors@usc.edu', 'localhost', 'ABC', '123')
