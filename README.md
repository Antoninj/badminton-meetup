## Description

Python script to automate the weekly registration to the brussels badminton meetups. Make sure you have at least python 3 to use the script.

## Setting up

First, you need to get your personal meetup API and TWILIO credentials. The TWILIO credentials are optional and only needed if you want to use the sms confirmation feature.

1. [Meetup API](https://secure.meetup.com/meetup_api/key/)
2. [Twilio API](https://www.twilio.com/console)

Once this is done, update the JSON configuration file with your personal information.


##  Automation

### Unix systems

* Open the terminal
* Edit the crontab using the following command:

```bash
crontab -e
```

* Add cronjobs. I suggest reading [this](https://en.wikipedia.org/wiki/Cron) to understand how to customize your cron jobs based on the days you want to register to.


Ex : cronjob to register for sundays events (the script needs to run on wednesdays after 22:00)

```bash
02 22 * * 3 python3 path/to/script/meetup_badminton.py -d 6 -r yes -g 0

```
