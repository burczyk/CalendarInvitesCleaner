import sqlite3
import os

def exit_calendar():
	os.system('killall Calendar')

def clean():
	home = os.environ.get('HOME')
	cache_path = '{0}/Library/Calendars/Calendar Cache'.format(home)
	conn = sqlite3.connect(cache_path)
	c = conn.cursor()
	c.execute('''DELETE FROM ZMESSAGE''')
	conn.commit()
	conn.close()

exit_calendar()
clean()