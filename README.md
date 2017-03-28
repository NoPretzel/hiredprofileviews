## What is it?

It's an external custom database agnostic (sqlite) API to Hired.com which allows you to both be notified of new profile views by potential employers and allow you to differentiate between old and new profile views more easily. Hired.com is a marketplace of where employers can (in reverse, per se) apply to prospects. I made it because I wasn't able to tell the difference between differing profile views on their site.

You can contribute to the project as you like. 

## Sample usage

```python
from hired import Hired
 
def notify_me(new_company):
    print(new_company)
    
with Hired('username', 'password', notify_me) as h:
    h.poll()
```

notify_me here is where you'd build your own notification function that gets called on each new profile view. The company data will come in the first and only argument in  every call as a dictionary:

```python
new_company = {
    'name' : 'Awesome Company',
    'link' : 'http://hired.com/company-name',
    'li_data' : ['random facts']
}
```

If you want, you can also pass in polling frequency per 10 minutes, along with the current cycle of employment you're dealing with. In essence this is where you'd differentiate between when you've gone live before vs the current cycle. The default is 0.

```python
Hired('username', 'password', notify_me, frequency=10, cycle_id=0)
```

Here is one that would send you an email on every notification via gmail's SMTP:

```python
import smtplib
from email.mime.text import MIMEText
 
def notify_me(company_data):
    gmail_login = 'gmail@gmail.com'
    gmail_pass = 'gmailpassword'

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
```

![Sample](https://i.imgur.com/xITfgEh.png)

Although keep in mind with the rise of oAuth, Gmail no longer considers plain-text password input  clients as secure (rightfully so). You'd have to manually disable this security feature. If you really want to use Gmail, I'd suggest using a throwaway account to send your main email the messages, or just forward all messages from that email to your main.

## Keeping in mind

The first batch will not notify you as you may already have many profile views on your account and you'd get hit with a ton of notifications. It'll only send you "new" profile views.

Also keeping in mind that this was all done for fun while I've been in between applications, so you probably shouldn't expect any magical consistency throughout updates of their website. Although I think updating this should be trivial considering the concentration of jobs available through Hired ;).
