#!/usr/bin/env python
#
# Very basic example of using Python and IMAP to iterate over emails in a
# gmail folder/label.  This code is released into the public domain.
#
# RKI July 2013
# http://www.voidynullness.net/blog/2013/07/25/gmail-email-with-python-via-imap/
#
import sys
import imaplib
import email
import email.header
import datetime
import account

EMAIL_FOLDER = "INBOX"


def process_mailbox(M):
    """
    Do something with emails messages in the folder.
    For the sake of this example, print some headers.
    """
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
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
        rv, data = M.search(None, "All")
        if rv != "OK":
            print "No messages found"
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
    print "Processing mailbox...\n"
    get_latest_email(M)
    M.close()
else:
    print "ERROR: Unable to open mailbox ", rv

M.logout()
