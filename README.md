# arXiv feed checker and mailer


## How to use
### Setup arXiv feed checker with private variables
Edit the variables in `private-file.py`.

Because your computer might not be running 24/7, I run this script multiple times per day (between 06:00 and 21:00 every hour). I do this by adding a cron job at my Raspberry Pi, by using `crontab -e` and then adding:
```
0 6-21/1 * * * /usr/bin/python /home/pi/arxiv-feed-mailer/send_arxiv.py >> /home/pi/arxiv-feed-mailer/send.log 2>&1
```

### Setup Google API
1. Follow [step 1: Turn on the Gmail API](https://developers.google.com/gmail/api/quickstart/python#step_1_turn_on_the_api_name) to create a `client_secret.json` file.
2. Install the Google Client Library with:
```
pip install --upgrade google-api-python-client feedparser
```
3. Run (add the `--noauth_local_webserver` flag if you work through `ssh`)
```
python gmailsendapi.py
```