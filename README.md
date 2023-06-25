# SlackBot

In this repro, we are creating a Slackbot by using Slack sdk!
I used Logzio to monitor my logs. You can use each ELK provider you'd prefer. 

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

Create a .env file with the following values:
```
SLACK_BOT_TOKEN= <'YOUR_SLACK_BOT_TOKEN'>
SLACK_APP_TOKEN = <'YOUR_SLACK_APP_TOKEN'>
SLACK_SIGNING_SECRET=<'YOUR_SLACK_SIGNING_SECRET'>
CHANNEL_ID = <'YOUR_CHANNEL_ID'>
LOGZIO_TOKEN =<'YOUR_LOGZIO_TOKEN'>
```

Finally - I used vercel to deploy my project. You can follow up with this video: 
https://www.youtube.com/watch?v=rnbQIQe2M4Y

![image](https://github.com/RefaelMizrahi/SlackBot/assets/74647294/0209fe3f-57c0-4e7f-b418-c2da4918cb3f)


What does the script do?
1. When the customer sends a message we reply back with the following response:
Hey there @user, I hope you're well. Thanks for reaching out!
We have opened a ticket regarding your request, and we will update you ASAP!
2. A ticket with the user id is being opened in the backend,  in our local  project under the tickets folder. 
3. We provide the customer with our documentation, with the following response:
4. The customer chooses the topic of the ticket BUG / FIX we reply back and update the ticket.
5. If the customer responds in the thread, we update the ticket as well 

![image](https://github.com/RefaelMizrahi/SlackBot/assets/74647294/2cdfbbdc-31ca-4bd1-8f1e-98334f13b3f9)

![image](https://github.com/RefaelMizrahi/SlackBot/assets/74647294/6e09c4ae-f035-41fd-9ca3-f6b2f90ff921)
