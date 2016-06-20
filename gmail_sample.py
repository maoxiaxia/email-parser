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
import datetime
import account
from email.Header import decode_header
from email.Parser import Parser as EmailParser
from email.utils import parseaddr
from base64 import b64decode
from StringIO import StringIO

EMAIL_FOLDER = "INBOX"


def parse_attachment(message_part):
    """Parse Email Attachment.

    parse attachment.
    """
    content_disposition = message_part.get("Content-Disposition", None)
    if content_disposition:
        dispositions = content_disposition.strip().split(";")
        if bool(content_disposition and
                dispositions[0].lower() == "attachment"):

                file_data = message_part.get_payload(decode=True)
                attachment = StringIO(file_data)
                attachment.content_type = message_part.get_content_type()
                attachment.size = len(file_data)
                attachment.name = None
                attachment.create_date = None
                attachment.mod_date = None
                attachment.read_date = None

                for param in dispositions[1:]:
                    name, value = param.split("=")
                    name = name.lower()

                    if name == "filename":
                        attachment.name = value
                    elif name == "create-date":
                        attachment.create_date = value  # TODO: datetime
                    elif name == "modification-date":
                        attachment.mod_date = value  # TODO: datetime
                    elif name == "read-date":
                        attachment.read_date = value  # TODO: datetime
                return attachment
    # no attachment
    return None


def process_mailbox(M):
    """.

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
    """.

    get the most recent received email.
    """
    data = search_email_by_time(M)
    if data is None:
        return
    print "Access data succeed"
    print "Got data as ", data
    ids = data[0]
    id_list = ids.split()
    if len(id_list) > 0:
        latest_email_id = id_list[-1]
        # search unique id
        rv, data = M.uid('fetch', latest_email_id, "(RFC822)")
        if rv != "OK":
            print "Error getting message"
            return
        # here's the body, which is raw text of the whole email
        # including headers and alternate payloads
        raw_email = data[0][1]
        print "raw_email is ", raw_email
        # print raw_email
        email_message = email.message_from_string(raw_email)
        print "To: ", email_message['To'], "\n"
        print "From: ", email.utils.parseaddr(email_message['From']), "\n"
        # print all headers
        # print email_message.items(), "\n"

        # print the body text
        print get_first_text_block(email_message)


def get_group_of_emails(M):
    """Get a group of emails.

    This function will access emails from a group of contacts.
    """
    print "Try to access group of emails"
    data = search_email_advanced(M)
    if data is None:
        return
    # print "Got data as ", data
    ids = data[0]
    id_list = ids.split()
    print id_list
    for id_num in id_list:
        rv, data = M.uid('fetch', id_num, "(RFC822)")
        if rv != "OK":
            print "Error getting message"
            return
        # get raw text of the whole email
        raw_email = data[0][1]
        print "*********raw data ", raw_email
        email_message = email.message_from_string(raw_email)
        # print "++++++++++transformed string is ", email_message
        # print sender and receivers
        print "To: ", email_message['To'], "\n"
        print "From: ", email.utils.parseaddr(email_message['From']), "\n"
        result = parse_content(email_message)
        # print results
        printData(result)


def printData(result):
    """Print parsed info.

    simple print statements.
    """
    print "Subject: \n", result['subject'], "\n"
    print "Body: \n", result['body']
    print "Html: \n", result['html']
    print "Attachments: \n", result['attachments']


def parse_subject(content):
    """Parse email subject.

    return subject.
    """
    parser = EmailParser()
    msgobj = parser.parse(content)
    if msgobj['Subject'] is not None:
        # email has subject
        decodefrag = decode_header(msgobj['Subject'])
        subj_fragments = []
        for s, enc in decodefrag:
            if enc:
                s = unicode(s, enc).encode('utf8', 'replace')
            subj_fragments.append(s)
        subject = ''.join(subj_fragments)
    else:
        subject = None
    return subject


def parse_content(email_message):
    """Get body text from a email.

    return the body.
    """
    attachments = []
    body = None
    html = None
    subject = parse_subject
    for part in email_message.walk():
        attachment = parse_attachment(part)
        if attachment:
            attachments.append(attachment)
        elif part.get_content_type() == "text/plain":
            if body is None:
                body = ""
            body += unicode(
                part.get_payload(decode=True),
                part.get_content_charset(),
                'replace'
                ).encode('utf8', 'replace')
        elif part.get_content_type() == "text/html":
            if html is None:
                html = ""
            html += unicode(
                part.get_payload(decode=True),
                part.get_content_charset(),
                'replace'
            ).encode('utf8', 'replace')
    # return the parsed data
    return {
        'subject': subject,
        'body': body,
        'html': html,
        'attachments': attachments
    }


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
    print "search emails in advanced mode"
    till_date = 360
    date_range = datetime.date.today() - datetime.timedelta(till_date)
    date = date_range.strftime("%d-%b-%Y")
    # rv, data = M.uid('search', None, \
    #    '(SENTSINCE {date} FROM "lmxvip@hotmail.com")'.format(date=date))
    rv, data = M.uid(
        'search',
        None,
        '(SENTSINCE {date} FROM "cindyyueweiluo@gmail.com")'
        .format(date=date)
        )
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

# Following is the program execution
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
    # process_mailbox(M)
    get_group_of_emails(M)
    M.close()
else:
    print "ERROR: Unable to open mailbox ", rv

M.logout()
