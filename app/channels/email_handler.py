import smtplib
import logging
import imaplib
import email
import os
import threading

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import MultiChannelException


logger = logging.getLogger(__name__)


class EmailHandler:

    def __init__(self, password, address, imap_server, host=None, database, port_smtp=587, port_imap=993):

        if host:
            self.server = smtplib.SMTP(host=host, port=port_smtp)
        else:
            raise MultiChannelException("Email server not configured")

        if imap_server:
            self.imap_server = imap_server
        else:
            raise MultiChannelException("Email server not configured")

        self.password = password
        self.user = address

        self.db = database

        self.inbox = EmailHandler._init_inbox(password, self.imap_server, address, port_imap)

        # TODO check if is always needed
        self._login()

    @staticmethod
    def _init_inbox(password, imap_server, address, port):
        """
        Setups email inbox
        """
        mail = imaplib.IMAP4_SSL(host=imap_server, port=port)
        mail.login(address, "{}".format(password))

        mail.select("INBOX", readonly=True)
        return mail

    def _login(self):
        self.server.starttls()
        self.server.login(user=self.user, password=self.password)

    def _quit(self):
        self.server.quit()

    def send_message(self, message, user, info):
        for receiver in message.receivers:
            toaddr = receiver.get("address")
            if message.message_type == "seen":
                formatted_message = self._format_message(toaddr, message.body, seen=True)
            else:
                formatted_message = self._format_message(toaddr, message.body)

            self.server.sendmail(self.user, to_addrs=toaddr, msg=formatted_message)

        return True

    def get_status(self, message_id):

        results, data = self.inbox.uid("search", None, "UNSEEN")
        id_list  = data[0].split()

        results = []
        for id_ in id_list:
            res, message = self.inbox.uid("fetch", id_, "(RFC822)")
            raw_message = message[0][1]
            parsed_email = self._parse_raw_email(raw_message, id_)
            results.append(parsed_email)

        if not results:
            return None

        return results

    def _parse_raw_email(self, raw_message):

        def get_body(msg):
            msg_type = msg.get_content_maintype()
            if msg_type == "text":
                return msg.get_payload()

            if msg_type != "multipart":
                logger.critical("Invalid email response format. Format: %s", msg_type)
                return ""

            for content in msg.get_payload():
                if content.get_content_maintype() == "text":
                    return content.get_payload()

            return ""

        subject = msg.get("subject")

        user_id = None
        message_id = None
        try:
            user_id = subject.split()[1]
            message_id = subject.split()[2]
        except Exception as e:
            logger.critical("Error during parsing. Error %s", e)

        if not all([message_id, user_id]):
            return None

        msg = email.message_from_string(raw_message)
        success = self.db.add_answer_to_message(message_id, user_id, msg)

        return success

    def _format_message(self, receiver, text, message_id, seen=False):
        message = MIMEMultipart("alternative")

        # handle the addresses
        message['From'] = self.user
        message['To'] = receiver

        message['Subject'] = "Multichannel {} {}".format(message_id, user_id)

        html_format = EmailHandler.create_html(text=text, seen=seen)
        html = MIMEText(html_format, "html")

        # TODO check if this is also needed
        plaintext = MIMEText(text.get("body"), "plaintext")

        message.attach(plaintext)
        message.attach(html)

        string = message.as_string()
        return string

    @staticmethod
    def create_html(text, seen=False):
        # TODO customize html format

        body = """ \
        <html>
            <head></head>
            <body>
                <p>{text}</p>
                <a href="{image}" download>
            </body>
        </html>
        """.format(text=text, image=EmailHandler._get_pixel() if seen else "")

        return body

    @staticmethod
    def _get_pixel():
        current = os.getcwd()
        try:
            path_to_image = os.path.join(current, "images/pixel.png")
            return path_to_image
        except Exception:
            logger.warning("Image not found")
            return ""
