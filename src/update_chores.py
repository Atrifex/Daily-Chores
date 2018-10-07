
import sys
from datetime import datetime
from pytz import timezone
import pytz
import sqlite3

# initialize database connection
con = sqlite3.connect('../data/home.db')
cur = con.cursor()

def get_user_id(user_name):
    cur.execute('SELECT id FROM user WHERE first_name = \'' + user_name + '\'')
    return cur.fetchone()[0]

def get_chore_id(chore_name):
    cur.execute('SELECT id FROM chore WHERE name = \'' + chore_name + '\'')
    return cur.fetchone()[0]

def get_chore_description(chore_name):
    cur.execute('SELECT description FROM chore WHERE name = \'' + chore_name + '\'')
    return cur.fetchone()[0]

def get_date_assigned(chore_id):
    cur.execute('SELECT date_assigned FROM chore_assignment WHERE chore_id = ' + str(chore_id))
    return cur.fetchone()[0]

def log_chore(user_name, chore_name):
    user_id = get_user_id(user_name)
    chore_id = get_chore_id(chore_name)
    date_assigned = get_date_assigned(chore_id)
    date_completed = str(datetime.now(timezone('US/Pacific')))

    cur.execute('INSERT INTO chore_log (user_id, chore_id, date_completed, date_assigned) VALUES (?, ?, ?, ?)', \
        (user_id, chore_id, date_completed, date_assigned))
    con.commit()

def reassign_chore(user, chore):
    cur.execute('SELECT COUNT (1) FROM user')
    user_count = cur.fetchall()[0][0]
    current_user_id = get_user_id(user)
    chore_id = get_chore_id(chore)
    next_user_id = (current_user_id + 1)%user_count
    date_assigned =  str(datetime.now(timezone('US/Pacific')))

    cur.execute('UPDATE chore_assignment SET user_id = ' + str(next_user_id) + ' WHERE chore_id = ' + str(chore_id))
    cur.execute('UPDATE chore_assignment SET date_assigned = \'' + date_assigned + '\' WHERE chore_id = ' + str(chore_id))
    con.commit()

def get_chore_assignments():
    cur.execute('SELECT user.first_name, chore.description FROM chore_assignment INNER JOIN chore ON chore_id = chore.id INNER JOIN user ON user_id = user.id')
    return cur.fetchall()

def compose_message(user, chore):
    message = user.title() + ' completed: ' + get_chore_description(chore) + '\n\n'
    message += 'Current Assignments:\n'
    assignments = get_chore_assignments()
    for assignment in assignments:
        message += assignment[0].title() + ' - ' + assignment[1] + '\n'

    return message

def send_notifications(message):
    cur.execute('SELECT phone_number FROM user')
    txt_manager = NotificationManager()

    for number in cur.fetchall():
        txt_manager.send_message(number[0], message)

def main():
    # extract names from command line input
    user = sys.argv[1].upper()
    chore = sys.argv[2].upper()

    # log chores
    log_chore(user, chore)

    # figure out new assignments based on
    reassign_chore(user, chore)

    # Notify all users of current state
    print(compose_message(user, chore))

    # close connection to database
    cur.close()
    con.close()

if __name__ == '__main__':
    main()
