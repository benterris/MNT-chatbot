import os
import sys
import time
from controller import Controller
from slackclient import SlackClient


controller = Controller()

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

def handle_message(message, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    user = channel
    response = controller.handle_message(message, user)

    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)



def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'type' in output \
            and 'desktop_notification' in output['type']\
            and '@everyone' not in output['content'] \
            and '@channel' not in output['content'] \
            and '@here' not in output['content']:
                # return text after the @ mention, whitespace removed
                # Channel va servir a obtenir un identifiant unique pour l'utilisateur qui parle.
                return output['content'].strip(), \
                       output['channel']
    return None, None

if __name__ == "__main__":

    READ_WEBSOCKET_DELAY = 0.1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("MNTbot connected and running!")
        while True:
            message, channel= parse_slack_output(slack_client.rtm_read())
            if message and channel:
                handle_message(message, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connexion failed. Invalid Slack token or bot ID?")
