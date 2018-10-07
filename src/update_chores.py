
import sys
from datetime import datetime
from pytz import timezone
import pytz
import sqlite3

# initialize database connection

class DatabaseManager(object):
    def __init__(self):
        self.con = sqlite3.connect('../data/home.db', check_same_thread=False)
        self.cur = self.con.cursor()

    def __del__(self):
        self.cur.close()
        self.con.close()

    def get_user_id(self, user_name):
        self.cur.execute('SELECT id FROM user WHERE first_name = \'' + user_name + '\'')
        return self.cur.fetchone()[0]

    def get_chore_id(self, chore_name):
        self.cur.execute('SELECT id FROM chore WHERE name = \'' + chore_name + '\'')
        return self.cur.fetchone()[0]

    def get_chore_description(self, chore_name):
        self.cur.execute('SELECT description FROM chore WHERE name = \'' + chore_name + '\'')
        return self.cur.fetchone()[0]

    def get_date_assigned(self, chore_id):
        self.cur.execute('SELECT date_assigned FROM chore_assignment WHERE chore_id = ' + str(chore_id))
        return self.cur.fetchone()[0]

    def log_chore(self, chore_name, user_name):
        user_id = self.get_user_id(user_name)
        chore_id = self.get_chore_id(chore_name)
        date_assigned = self.get_date_assigned(chore_id)
        date_completed = str(datetime.now(timezone('US/Pacific')))

        self.cur.execute('INSERT INTO chore_log (user_id, chore_id, date_completed, date_assigned) VALUES (?, ?, ?, ?)', \
            (user_id, chore_id, date_completed, date_assigned))
        self.con.commit()

    def reassign_chore(self, chore_name, user_name):
        self.cur.execute('SELECT COUNT (1) FROM user')
        user_count = self.cur.fetchall()[0][0]
        current_user_id = self.get_user_id(user_name)
        chore_id = self.get_chore_id(chore_name)
        next_user_id = (current_user_id + 1)%user_count
        date_assigned =  str(datetime.now(timezone('US/Pacific')))

        self.cur.execute('UPDATE chore_assignment SET user_id = ' + str(next_user_id) + ' WHERE chore_id = ' + str(chore_id))
        self.cur.execute('UPDATE chore_assignment SET date_assigned = \'' + date_assigned + '\' WHERE chore_id = ' + str(chore_id))
        self.con.commit()

    def get_chore_assignments(self):
        self.cur.execute('SELECT user.first_name, chore.description FROM chore_assignment INNER JOIN chore ON chore_id = chore.id INNER JOIN user ON user_id = user.id')
        return self.cur.fetchall()

    def compose_message(self, chore_name, user_name):
        message = user_name.title() + ' completed: ' + self.get_chore_description(chore_name) + '\n\n'
        message += 'Current Assignments:\n'
        assignments = self.get_chore_assignments()
        for assignment in assignments:
            message += assignment[0].title() + ' - ' + assignment[1] + '\n'

        return message

    def update_chore(self, chore_name, user_name):
        chore_name = chore_name.upper()
        user_name = user_name.upper()

        # log chores
        self.log_chore(chore_name, user_name)

        # figure out new assignments based on
        self.reassign_chore(chore_name, user_name)

        # Notify all users of current state
        message = self.compose_message(chore_name, user_name)

        return message

def main():
    # extract names from command line input
    chore = sys.argv[1]
    user = sys.argv[2]

    print(DatabaseManager().update_chore(chore, user))

if __name__ == '__main__':
    main()
