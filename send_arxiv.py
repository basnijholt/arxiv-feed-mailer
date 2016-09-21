#!/usr/bin/env python

from __future__ import print_function
import os
from gmailsendapi import send_message, create_message
import datetime
import re
import feedparser
from private_variables import (title_words, abstract_words,
                               author_words, feed_url, my_mail)

file_path = os.path.dirname(os.path.abspath(__file__))
now = datetime.datetime.now()
date_str = str(now.date())

def filter(entry):
    return (any([word in entry.summary.lower() for word in abstract_words])
            or any([author in entry.author.lower() for author in author_words])
            or any([titleword in entry.title.lower() for titleword in title_words + abstract_words]))


def strip_html(text):
    """See http://stackoverflow.com/a/9662362"""
    return re.sub('<[^<]+?>', '', text)


def get_arxiv_mail(title_words, abstract_words, 
                   author_words, feed_url, my_mail):
    feed = feedparser.parse(feed_url)
    filtered_entries = [entry for entry in feed.entries if filter(entry)]

    msg = ["<h1>arXiv results for {}</h1>".format(date_str)]

    for entry in filtered_entries:
        msg.append('<h2>{}</h2>'.format(entry.title))
        msg.append('<h3>{}</h3>'.format(strip_html(entry.author)))
        msg.append('<p>{}</p>'.format(strip_html(entry.description)))
        num = 'arXiv:' + entry['id'].split('/')[-1]
        link = '<a href="{}">{}</a>'.format(entry['id'], num)
        pdf_link = '[<a href="{}">pdf</a>]'.format(entry.id.replace('abs', 'pdf'))
        msg.append(link + " " + pdf_link)
    keywords = ', '.join(title_words + abstract_words)
    authors = ', '.join(author_words)
    footer = ("<p><em>Selected keywords: {}. Selected authors: {}. " +
              "From feed: {}</em></p>")
    msg.append(footer.format(keywords, authors, feed_url))
    msg = "".join(msg)
    return msg


def send_todays_arxiv(sender, to):
    message_text = get_arxiv_mail(title_words, abstract_words,
                                  author_words, feed_url, my_mail)
    subject = "Today's arXiv {}".format(date_str)
    message = create_message(sender, to, subject, message_text)
    send_message(message)


if __name__ == "__main__":
    # execute only if run as a script
    send_file = os.path.join(file_path, 'send.txt')
    if not os.path.exists(send_file):
        # Create send.txt if it doesn't exist
        open(send_file, 'w').close()

    with open(send_file, 'r') as f:
        # Read the date when the last email was sent.
        send_file_date = f.read()


    if send_file_date == date_str:
        # Don't send if mail is already sent.
        print("Already sent")
    else:
        send_todays_arxiv(my_mail, my_mail)
        print("Send time is {}".format(str(now.time())))
        with open(send_file, 'w') as f:
            f.write(date_str)
