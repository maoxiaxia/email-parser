#!/usr/bin/env python
#
# Very basic example of using Python and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# RKI July 2013
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#

"""This module implements an email parser to access targeted info."""

import sys
import imaplib
import email
import email.header
import datetime
import account

EMAIL_FOLDER = "INBOX"


def process_mailbox(M):
    """.

    Do something with emails messages in the folder.
    For the sake of this example, print some headers.
    """
    data = search_email_advanced(M)
    if data is None:
        print "ERROR accessing data."
        return

    ids = data[0]
    id_list = ids.split()
    for num in id_list:
        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return

        msg = email.message_from_string(data[0][1])
        decode = email.header.decode_header(msg['Subject'])[0]
        subject = unicode(decode[0])
        print 'Message %s: %s' % (num, subject)
        print 'Raw Date:', msg['Date']
        # Now convert to local date-time
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print "Local Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S")


def get_latest_email(M):
    """.

    get the most recent received email.
    """
    # basic search mode
    # data = search_email_by_all(M)
    # data = search_email_by_time(M)
    data = search_email_advanced(M)
    if data is None:
        return
    ids = data[0]
    id_list = ids.split()
    latest_email_id = id_list[-1]
    # search unique id
    rv, data = M.uid('fetch', latest_email_id, "(RFC822)")
    if rv != "OK":
        print "Error getting message"
        return
    # here's the body, which is raw text of the whole email
    # including headers and alternate payloads
    raw_email = data[0][1]
    # print raw_email
    email_message = email.message_from_string(raw_email)
    print "To: ", email_message['To'], "\n"
    print "From: ", email.utils.parseaddr(email_message['From']), "\n"
    # print all headers
    # print email_message.items(), "\n"

    # print the body text
    print get_first_text_block(email_message)


def get_first_text_block(email_message_instance):
    """.

    retrieve the text block in the email body
    """
    maintype = email_message_instance.get_content_maintype()
    if maintype == 'multipart':
        for part in email_message_instance.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
    elif maintype == 'text':
        return email_message_instance.get_payload()


def search_email_by_all(M):
    """.

    basic search mode, search all
    """
    print "basic search mode\n"
    rv, data = M.uid('search', None, 'All')
    if check_response(rv):
        return data
    else:
        return None


def search_email_by_time(M):
    """.

    search email by time
    """
    print "search mail by time\n"
    date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
    rv, data = M.uid('search', None, '(SENTSINCE {date})'.format(date=date))
    if check_response(rv):
        return data
    else:
        return None


def search_email_advanced(M):
    """.

    limit search by date, subject, and exclude a sender
    """
    print "more advanced search mode\n"
    date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
    rv, data = M.uid('search', None, '(SENTSINCE {date} HEADER Subject "My"\
    "Subject" FROM "coders@codingame.com")'.format(date=date))

    if check_response(rv):
        return data
    else:
        return None


def check_response(rv):
    """.

    check whether response is OK or not
    return true if it's OK
    return false otherwise.
    """
    if rv != 'OK':
        print "No message found"
        return False
    return True


# try to log into account
M = imaplib.IMAP4_SSL('imap.gmail.com')

try:
    rv, data = M.login(account.EMAIL_ACCOUNT, account.EMAIL_PSS)
except imaplib.IMAP4.error:
    print "LOGIN FAILED!!! "
    sys.exit(1)

print rv, data

rv, mailboxes = M.list()
if rv == 'OK':
    print "Mailboxes:"
    print mailboxes

rv, data = M.select(EMAIL_FOLDER)
if rv == 'OK':
    print "Processing mailbox INBOX...\n"
    # get_latest_email(M)
    process_mailbox(M)
    M.close()
else:
    print "ERROR: Unable to open mailbox ", rv

M.logout()
