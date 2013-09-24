#!/usr/bin/env python

"""
Mail Merge helps you clear your inbox.

Usage:
    mailMerge email
    mailMerge name
    mailMerge domain
    mailMerge subject
"""

from docopt import docopt

import contextio
import pprint
import settings


def merge_by_sender_email(message):
    return message.addresses['from']['email']


def merge_by_sender_name(message):
    sender = message.addresses['from']
    if 'name' in sender:
        key = 'name'
    else:
        key = 'email'
    return sender[key]


def merge_by_domain(message):
    # return domain name
    return message.addresses['from']['email'].split('@')[1]


def merge_by_subject(message):
    # return three words of the subject
    return ' '.join(message.subject.split(' ')[1:4])


def choose_merge(args):
    if args['email']:
        return merge_by_sender_email
    elif args['name']:
        return merge_by_sender_name
    elif args['domain']:
        return merge_by_domain
    else:
        return merge_by_subject


def main(args):
    merge_by = choose_merge(args)

    cio = contextio.ContextIO(
        consumer_key=settings.CONSUMER_KEY,
        consumer_secret=settings.CONSUMER_SECRET)

    account = cio.get_accounts()[0]

    merged = {}

    has_messages = True
    page = 0
    while has_messages:
        print(page)
        offset = page * 25
        messages = account.get_messages(folder='inbox', offset=offset)
        has_messages = len(messages) != 0

        for message in messages:
            key = merge_by(message)
            if key not in merged:
                merged[key] = 0
            merged[key] += 1

        page += 1

    sortedMerged = sorted(
        list(merged.iteritems()),
        key=lambda x: x[1],
        reverse=True)
    pprint.pprint(sortedMerged[:20])

if __name__ == '__main__':
    args = docopt(__doc__)
    main(args)
