#!/usr/bin/env python
# vim: et ts=4 sw=4

import imaplib
import email
from django.contrib.auth.models import User
from hunchworks.models import Evidence


class ImapAgent(object):
    def __init__(self, name, host, username, password):
        self._user, created = User.objects.get_or_create(
            username=name)

        self._imap = imaplib.IMAP4_SSL(host)
        self._imap.login(username, password)

    def poll(self):
        self._imap.select("INBOX")
        for message in self._messages():

            print "Message from %s: %s" % (
                message["from"], message["subject"])

            Evidence.objects.create(
                title=message["subject"],
                description=message.get_payload(),
                creator=self._user.get_profile())

    def _messages(self):
        result, data = self._imap.uid("search", None, "UNSEEN")
        return [self._fetch(uid) for uid in data if uid != ""]

    def _fetch(self, uid):
        result, data = self._imap.uid("fetch", uid, "(RFC822)")
        return email.message_from_string(data[0][1])