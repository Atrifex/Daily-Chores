
import sys
from datetime import datetime
from pytz import timezone
import pytz
import sqlite3

# initialize database connection
con = sqlite3.connect('../data/home.db', check_same_thread=False)
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

def log_chore(chore_name, user_name):
    user_id = get_user_id(user_name)
    chore_id = get_chore_id(chore_name)
    date_assigned = get_date_assigned(chore_id)
    date_completed = str(datetime.now(timezone('US/Pacific')))

    cur.execute('INSERT INTO chore_log (user_id, chore_id, date_completed, date_assigned) VALUES (?, ?, ?, ?)', \
        (user_id, chore_id, date_completed, date_assigned))
    con.commit()

def reassign_chore(chore_name, user_name):
    cur.execute('SELECT COUNT (1) FROM user')
    user_count = cur.fetchall()[0][0]
    current_user_id = get_user_id(user_name)
    chore_id = get_chore_id(chore_name)
    next_user_id = (current_user_id + 1)%user_count
    date_assigned =  str(datetime.now(timezone('US/Pacific')))

    cur.execute('UPDATE chore_assignment SET user_id = ' + str(next_user_id) + ' WHERE chore_id = ' + str(chore_id))
    cur.execute('UPDATE chore_assignment SET date_assigned = \'' + date_assigned + '\' WHERE chore_id = ' + str(chore_id))
    con.commit()

def get_chore_assignments():
    cur.execute('SELECT user.first_name, chore.description FROM chore_assignment INNER JOIN chore ON chore_id = chore.id INNER JOIN user ON user_id = user.id')
    return cur.fetchall()

def compose_message(chore_name, user_name):
    message = user_name.title() + ' completed: ' + get_chore_description(chore_name) + '\n\n'
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

def update_chore(chore_name, user_name):
    chore_name = chore_name.upper()
    user_name = user_name.upper()

    # log chores
    log_chore(chore_name, user_name)

    # figure out new assignments based on
    reassign_chore(chore_name, user_name)

    # Notify all users of current state
    message = compose_message(chore_name, user_name)

    # close connection to database
    cur.close()
    con.close()

    return message

def main():
    # extract names from command line input
    chore = sys.argv[1]
    user = sys.argv[2]

    print(update_chore(chore, user))

if __name__ == '__main__':
    main()
