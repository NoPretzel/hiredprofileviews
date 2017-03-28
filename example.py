from hired import Hired
import smtplib
from email.mime.text import MIMEText


def notify_me(company_data):
    gmail_login = 'gmail@gmail.com'
    gmail_pass = 'gmailpass'

    message = """<p>You have a new profile view from {}. You can read more about their company <a href="{}">here</a>.</p>

    <p>Some random facts about the company:</p>
    <ol>
    """.format(company_data['name'], company_data['link']) +\
    "".join(["<li>"+li+"</li>" for li in company_data['li_data']]) + "</ol>"

    email = MIMEText(message, 'html')
    email['Subject'] = "New profile view from {}".format(company_data['name'])
    email['From'], email['Reply-to'], email['To'] = [gmail_login] * 3
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(gmail_login, gmail_pass)
    server.sendmail(gmail_login, gmail_login, email.as_string())
    server.close()

with Hired('hiredemail', 'hiredpass', notify_me) as h:
    h.poll()
