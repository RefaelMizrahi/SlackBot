import os
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from pathlib import Path
from dotenv import load_dotenv
import logging
import logging.config
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from tickets import save_to_file
from tickets import update_ticket 


#takes the token from the dirctory path /env
env_path = Path('.') / '.env'

#loading the environment 
load_dotenv(dotenv_path=env_path)

# Initializes your app with your bot token and socket mode handler
slack_bot_token = os.environ.get('SLACK_BOT_TOKEN')
slack_user_token = os.environ.get('SLACK_USER_TOKEN')
app = App(token=slack_bot_token)
channel_id = os.environ.get('CHANNEL_ID')
logzio_token = os.environ.get('LOGZIO_TOKEN')
slack_app = WebClient(token=slack_bot_token)
slack_app_token = os.environ["SLACK_APP_TOKEN"]
#sending logs to my logzio account
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'logzioFormat': {
            'format': '{"additional_field": "value"}',
            'validate': False
        }
    },
    'handlers': {
        'logzio': {
            'class': 'logzio.handler.LogzioHandler',
            'level': 'INFO',
            'formatter': 'logzioFormat',
            'token': logzio_token,
            'logzio_type': 'support_slack_bot',
            'logs_drain_timeout': 5,
            'url': 'https://listener.logz.io:8071',
            'retries_no': 4,
            'retry_timeout': 2,
            'add_context': True
        }
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['logzio'],
            'propagate': True
        }
    }
}
logging.config.dictConfig(LOGGING)
logger = logging.getLogger('SupportBotSigg')
#current path
baseDir = [os.path.dirname(os.path.abspath(__file__))][-1]
client = WebClient(token=slack_bot_token)

def send_documentation_menu(channel):
    options = [
        {"text": "Plans", "value": "plans","url":"https://docs.stigg.io/docs/plans"},
        {"text": "modeling your pricing", "value": "modeling-your-pricing", "url":"https://docs.stigg.io/docs/modeling-your-pricing"},
        {"text": "features", "value": "FR","url": "https://docs.stigg.io/docs/features"}
    ]
    actions = [
        {
            "name": "menu_options",
            "text": option["text"],
            "url":option.get('url'),
            "type": "button",
            "value": option["value"]
        } for option in options
    ]

    attachments = [
        {
            "text": """While we're working on your ticket, we offer you also to check our documentation.
    You can check out our main topics here:""",
            "fallback": "Unable to display menu",
            "callback_id": "menu_options",
            "color": "#3AA3E3",
            "attachment_type": "default",
            "actions": actions
        }
    ]

    try:
        response = client.chat_postMessage(channel=channel, attachments=attachments)
    except SlackApiError as e:
        logger.error(f"Error sending menu message: {e.response['error']}")
    return response

def creating_a_ticket(event):

    ticket = {}
    ticket_id = event.get("client_msg_id")
    ticket_user = event.get("user")
    ticket_text = event.get("text")
    ticket_creation = event.get('event_ts')
    #save the ticket in the local script under the tickets folder
    tickets_path = f"{baseDir}/tickets"
    ticket["ticket_id"] = ticket_id
    ticket["user"] = ticket_user
    ticket["text"] = ticket_text
    ticket["ticket_creation"] = ticket_creation
    #make sure we're updateing the ticket if it's a thread
    if event.get("thread_ts"):
        logger.info(f'updated a ticket: {ticket_user}')
        update_ticket(f"{tickets_path}/{ticket_user}","thread_ts", ticket,)
    else:    
        logger.info(f'created ticket: {ticket_user}')
        save_to_file(ticket,f"{ticket_user}.json",tickets_path)


# Listens to incoming messages
@app.message()
def message_hello(message, say):
    
    # say() sends a message to the channel where the event was triggered
    say(f"""Hey there <@{message['user']}>, I hope you're well. Thanks for reaching out!
We have opened a ticket regarding your request, and we will update you ASAP!""")

    user_from_slack = message['user']
    logger.info(f'A {user_from_slack} opened a ticket')
    creating_a_ticket(event=message)
    send_documentation_menu(channel_id)
    create_ticket_buttons(channel_id)
    logger.info("Menu message sent successfully.")
    logger.info(message)


# Function to create the ticket buttons
def create_ticket_buttons(channel_id):
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Please choose the type of ticket:"
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Bug Ticket"
                    },
                    "action_id": "bug_ticket"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "FR Ticket"
                    },
                    "action_id": "fr_ticket"
                }
            ]
        }
    ]

    app.client.chat_postMessage(
        channel=channel_id,
        blocks=blocks
    )




# Function to handle the bug ticket button action
@app.action("bug_ticket")
def handle_bug_ticket(ack, body):
    ack()
    # Send a thank you message for bug ticket in the main thread
    message = f"Thank you for reporting the bug! We'll look into it. 🐛"
    client.chat_postMessage(channel=channel_id, text=message)
    user = body['user']['id']
    ticket = f"{baseDir}/tickets/{user}"
    updapte = update_ticket(ticket, "ticket_type", "bug")
    if updapte:
        logger.info("successfuly update a ticket")
    else:
        logger.error("can't update a file")
    



    logger.info(f"body: {body}")
    logger.info(message)

# Function to handle the FR ticket button action
@app.action("fr_ticket")
def handle_fr_ticket(ack, body):
    ack()
    channel_id = body['channel']['id']

    # Send a thank you message for feature request ticket in the main thread
    message = f"Thank you for your feature request! We'll consider it for future updates. ✨"
    client.chat_postMessage(channel=channel_id, text=message)
    user = body['user']['id']
    ticket = f"{baseDir}/tickets/{user}"
    updapte = update_ticket(ticket, "ticket_type", "FR")
    if updapte:
        logger.info("successfuly update a ticket")
    else:
        logger.error("can't update a file")

    logger.info(body)
    logger.info(message)

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, slack_app_token).start()
    