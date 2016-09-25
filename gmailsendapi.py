#!/usr/bin/env python

from __future__ import print_function
import httplib2
import os
from apiclient import discovery
import oauth2client
import argparse
import base64
from email.mime.text import MIMEText
import sys
from private_variables import my_mail

python_version = sys.version_info.major

flags = argparse.ArgumentParser(
    parents=[oauth2client.tools.argparser]).parse_args()

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'mail-script.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = oauth2client.client.flow_from_clientsecrets(
            CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = oauth2client.tools.run_flow(flow, store, flags)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_service():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    return service


def create_message(sender, to, subject, message_text, style='html'):
    """Create a message for an email.

    Args:
      sender: Email address of the sender.
      to: Email address of the receiver.
      subject: The subject of the email message.
      message_text: The text of the email message.

    Returns:
      An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text, _subtype=style)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    message = message.as_string()
    if python_version == 2:
        message = base64.urlsafe_b64encode(message)
    else:
        message = base64.urlsafe_b64encode(
            message.encode('utf-8')).decode('utf-8')
    return {'raw': message}


def send_message(message):
    """Send an email message.

    Args:
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    service = get_service()
    message = service.users().messages().send(userId='me', body=message).execute()
    print('Message Id: %s' % message['id'])
    return message


if __name__ == '__main__':
    message = create_message(sender='',
                             to=my_mail,
                             subject='Test message succeeded',
                             message_text='Test message')

    send_message(message)
    print("You should have received a test message now.")
