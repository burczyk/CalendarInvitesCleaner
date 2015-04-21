#Clean pending OS X Calendar invites

When you have OS X **Calendar.app** configured to use google CalDAV calendars (e.g. for your custom domain) it collects more and more invites that you cannot get rid of.

![Pending calendar invites](https://raw.githubusercontent.com/burczyk/CalendarInvitesCleaner/master/assets/pending_invites.png)

I created simple python script that removes these pending invites.

##Code

The script itself can be found in file [https://github.com/burczyk/CalendarInvitesCleaner/blob/master/clean_calendar_invites.py](https://github.com/burczyk/CalendarInvitesCleaner/blob/master/clean_calendar_invites.py) or you can copy it from below:

```python
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
```

##Running

```bash
$ python clean_calendar_invites.py
```

##Abstract

All invites are stored in SQLite database under path `~/Library/Calendars/Calendar Cache`. 

The tricky part is that it's actually Core Data file and it uses [Write-Ahead Logging](http://www.sqlite.org/wal.html). When you open **Calendar.app** you can sometimes see `Calendar Cache-wal` and `Calendar Cache-shm` files under given path for a short time. 

This mechanism was introduced in iOS 7 and OS X Mavericks as [New default journaling mode for Core Data SQLite stores](https://developer.apple.com/library/ios/qa/qa1809/_index.html). In consequence such SQLite files stopped working with [SQLite Database Browser](http://sqlitebrowser.org). That's why some time ago so I switched to [SQLite Free - Datum](https://itunes.apple.com/us/app/sqlite-free-datum/id901631046?mt=12) (currently I see that original project was forked and restored, so maybe it works again).

When you open `Calendar Cache` file you'll see tables on the left and data on the right. We're interested in `ZMESSAGE` table which contains actual invites.

![ZMESSAGE table](https://raw.githubusercontent.com/burczyk/CalendarInvitesCleaner/master/assets/Calendar_Cache.png)

> Don't be surprised by `Z` prefix. It's added to each model by Core Data.

You can remove entries by yourself, but that's exactly what our script is doing.

The only additional thing is that it quits **Calendar.app** if it's running in the background.

After you run the script just restart the **Calendar.app**. Some invites may still be pending. In my case they are not accepted nor rejected yet, so they are re-downloaded when Calendar starts. With these I'm afraid we cannot deal.

##Do you like it?
Do you like this article? Share it on Twitter, Facebook, Google+ or anywhere you like so that more of us can benefit from it. Thanks!