# SlackBot

In this repro, we are creating a Slackbot by using Slack sdk!
I used Logzio to monitor my logs. 

Let's start!
You need to follow up with this guide to create your app in Slack:
https://slack.dev/bolt-python/tutorial/getting-started

Afterward - please install the requirements by using the command to install all of the Python modules and packages listed:
```bash
pip install -r requirements.txt 
```
You can create a trial account at Logzio with 5GB and 14 days of retention:
https://logz.io/

You need to send logs from Python: 
https://github.com/logzio/logzio-python-handler
```
Create a .env file and save all the tokens:
SLACK_BOT_TOKEN= <'YOUR_SLACK_BOT_TOKEN'>
SLACK_APP_TOKEN = <'YOUR_SLACK_APP_TOKEN'>
SLACK_SIGNING_SECRET=<'YOUR_SLACK_SIGNING_SECRET'>
CHANNEL_ID = <'YOUR_CHANNEL_ID'>
LOGZIO_TOKEN =<'YOUR_LOGZIO_TOKEN'>
```

How it looks in actions:
We're going to reply to every message that the customer sends and save it as a file in our local  project under the tickets folder, we saved the thread message and update the ticket, we saved the type of the ticket FR/BUG and update the ticket. 

