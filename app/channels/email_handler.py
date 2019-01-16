import smtplib
import logging
import imaplib
import email
import os
import threading

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


logger = logging.getLogger(__name__)


class EmailHandler:

    def __init__(self, password, address, imap_sever, database, host=None, port=587):

        if host:
            self.server = smtplib.SMTP(host=host, port=port)
        else:
            self.server = smtplib.SMTP("smtp.gmail.com", port=587)

        self.db = database
        self.imap_server = imap_sever
        self.password = password
        self.user = address

        self.inbox = EmailHandler._init_inbox(password, imap_sever, address)

        # TODO check if is always needed
        self._login()

    @staticmethod
    def _init_inbox(password, imap_server, address):
        """
        Setups email inbox
        """
        mail = imaplib.IMAP4_SSL(host=imap_server)
        mail.login(user=address, password=password)

        mail.select("INBOX", readonly=True)
        return mail

    def _login(self):
        self.server.starttls()
        self.server.login(user=self.user, password=self.password)

    def _quit(self):
        self.server.quit()

    def send_message(self, text, receivers, msg_type, sender_id):
        for receiver in receivers:
            toaddr = receiver.get("address")
            if msg_type == "seen":
                formatted_message = self._format_message(toaddr, text, seen=True)
            else:
                formatted_message = self._format_message(toaddr, text)

            self.server.sendmail(self.user, to_addrs=toaddr, msg=formatted_message)

        return True

    def get_status(self, message_id):

        def update_databse(*args):
            for result in args[0]:
                try:
                    self.db.update_messages(result)
                except Exception as e:
                    logger.critical("Database could not be updated. Error: %s", e)

        results, data = self.inbox.uid("search", None, "UNSEEN")
        id_list  = data[0].split()

        results = []
        for id_ in id_list:
            res, message = self.inbox.uid("fetch", id_, "(RFC822)")
            raw_message = message[0][1]
            parsed_email = self._parse_raw_email(raw_message, id_)
            results.append(parsed_email)

        if not results:
            return False

        threading.Thread(target=update_databse, args=results).start()
        return True

    @staticmethod
    def _parse_raw_email(raw_message, id_):

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

        msg = email.message_from_string(raw_message)
        _return_value = {
            "id": id_,
            "title": msg.get("subject"),
            "sender": email.utils.parseaddr(msg.get("to")),
            "receiver": email.utils.parseaddr(msg.get("from")),
            "body": get_body(msg)
        }

        return _return_value

    def _format_message(self, receiver, text, seen=False):
        message = MIMEMultipart("alternative")

        # handle the addresses
        message['From'] = self.user
        message['To'] = receiver

        message['Subject'] = text.get("subject")

        html_format = EmailHandler.create_html(text=text.get("body", ""), seen=seen)
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
