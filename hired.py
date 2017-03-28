import requests
import re
from database import Database
import time


class Hired:

    hired_homepage = "https://hired.com"
    hired_login_page = "https://hired.com/login"
    hired_visitors_page = "https://hired.com/profile/visitors"

    def __init__(self, username, password, notify_function, frequency=5, cycle_id=0, sqlite_file="Hired.db"):
        self.username = username
        self.password = password
        self.frequency = frequency
        self.cycle = cycle_id

        self.notify_me = notify_function

        self.db = Database(sqlite_file)
        self.first_run = self.db.is_first_run()
        self.db.initialize_db()

        self.session = requests.session()

        if not self.login():
            raise Exception("Login failed")

        print("Success!")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()

    def login(self):
        print("Logging In...")
        login_page = self.session.get(self.hired_login_page).text
        auth_token = re.search('name="csrf-token" content="(.*?)"', login_page).group(1)

        data = {
            'user[email]' : self.username,
            'user[password]' : self.password,
            'authenticity_token' : auth_token,
            'user[remember_me]:' : 0
        }

        signed_in = self.session.post(self.hired_login_page, data=data).text

        return signed_in.find('candidate-home-page') != -1

    def poll(self):
        try:
            while True:
                print("Polling data...")
                visitors_page = self.session.get(self.hired_visitors_page).text
                companies = re.findall("<div class='layout'>(.*?)</p></div>", visitors_page, re.DOTALL)
                company_data = []

                for company_html in companies:
                    name = re.search('select=">(.*?)<', company_html).group(1)
                    link = re.search('href="(.*?)"', company_html).group(1)
                    li_data = re.findall("<li class='inline-list__item'>(.*?)</li>", company_html, re.DOTALL)
                    company_data.append({
                        'name' : name,
                        'link' : self.hired_homepage+link,
                        'li_data' : li_data
                    })

                for company in company_data:
                    if not self.db.check_if_viewed(company['name'], self.cycle):
                        self.db.add_new_view(company['name'], self.cycle)
                        if not self.first_run:
                            self.notify_me(company)
                self.first_run = False
                print("Sleeping...")
                time.sleep(60 * 10 / self.frequency)
        except KeyboardInterrupt:
            return
