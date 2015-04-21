#Clean pending OS X Calendar invites

When you have OS X **Calendar.app** configured to use google CalDAV calendars (e.g. for your custom domain) it collects more and more invites that you cannot get rid of.

![Pending calendar invites]()

I created simple script in python that removes these pending invites.

##Code

The script itself can be found on [GitHub]() or you can copy it from below:

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

##Abstract

All invites are stored in SQLite database under path `~/Library/Calendars/Calendar Cache`. The tricky part is that it's actually Core Data file and it uses [Write-Ahead Logging](http://www.sqlite.org/wal.html). When you open **Calendar.app** you can sometimes see `Calendar Cache-wal` and `Calendar Cache-shm` files under given path. It was introduced in iOS 7 and OS X Mavericks as [New default journaling mode for Core Data SQLite stores](https://developer.apple.com/library/ios/qa/qa1809/_index.html). It stopped working with [SQLite Database Browser](http://sqlitebrowser.org) some time ago so I switched to [SQLite Free - Datum](https://itunes.apple.com/us/app/sqlite-free-datum/id901631046?mt=12) (currently I see that original project was forked and restored, so maybe it works again).

When you open `Calendar Cache` file you'll see tables on the left and data on the right. We're interested in `ZMESSAGE` table which contains invites.

> Don't be surprised of `Z` prefix. It's added to each model by Core Data.

You can remove them yourself, but that's exactly what our script is doing.

The only additional thing is that it quits **Calendar.app** if it's running in the background.

Simple and useful :)