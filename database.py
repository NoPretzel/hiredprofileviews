import sqlite3


class Database:

    def __init__(self, file):
        self.conn = sqlite3.connect(file)

    def close(self):
        self.conn.close()

    def is_first_run(self):
        c = self.conn.cursor()
        c.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="profile_views"')
        rows = c.fetchall()
        if len(rows) > 0:
            return False
        return True

    def initialize_db(self):
        c = self.conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS profile_views( view_id INTEGER PRIMARY KEY, company_name VARCHAR(100), cycle INT )')
        self.conn.commit()

    def check_if_viewed(self, company, cycle):
        c = self.conn.cursor()
        c.execute('SELECT * FROM profile_views where company_name = ? and cycle = ?', (company, cycle,))
        rows = c.fetchall()
        if len(rows) > 0:
            return True
        return False

    def add_new_view(self, company, cycle):
        c = self.conn.cursor()
        c.execute('INSERT INTO profile_views(company_name, cycle) VALUES (?, ?)', (company, cycle,))
        self.conn.commit()
        return True
