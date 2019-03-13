import smtplib
import logging
import imaplib
import email

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils import MultiChannelException


logger = logging.getLogger(__name__)


class EmailHandler:

    def __init__(self, password, address, imap_server, database, flask_server_url, host=None, port_smtp=587, port_imap=993):

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
        self.flask_server_url = flask_server_url
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

    def send_message(self, message, users):
        id_ = message.get("_id")

        results = []
        for user in users:
            toaddr = user.get("channels").get("email").get("address")
            if not toaddr:
                continue
            user_id = user.get("_id")
            _seen = message.get("type") == "traced"
            formatted_message = self._format_message(toaddr, text=message.get("message"), message_id=id_, user_id=user_id, seen=_seen)

            success = False
            try:
                self.server.sendmail(self.user, to_addrs=toaddr, msg=formatted_message)
                success = True
            except Exception as e:
                logger.warning("Error %s during sending", e)

            if not success:
                continue

            results.append(user.get("_id"))

        return results

    def get_updates(self):
        results, data = self.inbox.uid("search", None, "UNSEEN")
        id_list  = data[0].split()
        results = []
        for id_ in id_list:
            res, message = self.inbox.uid("fetch", id_, "(RFC822)")
            raw_message = message[0][1]
            parsed_email = self._parse_raw_email(raw_message)
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

        if isinstance(raw_message, bytes):
            raw_message = raw_message.decode("utf-8")

        msg = email.message_from_string(raw_message)

        subject = msg.get("subject")
        if "Multichannel" not in subject:
            return None

        answer = get_body(msg)
        if not answer:
            return None

        # Quick parse to remove the quote part as well as possible
        try:
            answer = [
                l for l in answer.splitlines()
                if not l.startswith('>') and self.user not in l and l
            ]
            answer = answer[:-1] if answer[-1].endswith(':') else answer
            answer = "\n".join(answer)
        except Exception as e:
            logger.warning("Could not clean up the answer.")
            answer = get_body(msg)

        user_id = None
        message_id = None
        try:
            subject = subject[3:].strip() if subject.lower().startswith("re:") else subject.strip()
            # subject.split()[0] is multichannel-text
            message_id = subject.split()[1]
            user_id = subject.split()[2]
        except Exception as e:
            logger.critical("Error during parsing. Error %s", e)

        if not user_id or not message_id:
            return None

        if isinstance(user_id, bytes):
            user_id = user_id.decode("utf-8")
        if isinstance(message_id, bytes):
            message_id = message_id.decode("utf-8")

        try:
            success = self.db.add_answer_to_message(message_id=message_id, user_id=user_id, answer=answer)
        except Exception as e:
            return None

        return success

    def _format_message(self, receiver, text, message_id, user_id, seen=False):

        message = MIMEMultipart("alternative")

        # handle the addresses
        message['From'] = self.user
        message['To'] = receiver

        message['Subject'] = "Multichannel {} {}".format(message_id, user_id)

        html_format = self.create_html(
            text=text,
            seen=seen,
            message_id=message_id,
            user_id=user_id,
        )
        html = MIMEText(html_format, "html")

        # TODO check if this is also needed
        plaintext = MIMEText(text, "plaintext")

        message.attach(plaintext)
        message.attach(html)

        string = message.as_string()
        return string

    def create_html(self, text, message_id, user_id, seen=False):
        # TODO customize html format
        if seen:
            image_html = "<img src={}>".format(self._get_pixel(message_id, user_id))
        else:
            image_html = ""
        body = """ \
        <html>
            <head></head>
            <body>
                <p>{text}</p>
                {image}
            </body>
        </html>
        """.format(text=text, image=image_html)

        return body

    def _get_pixel(self, message_id, user_id):
        return "http://{server}/api/messages/{message_id}/{user_id}".format(
            server=self.flask_server_url,
            message_id=message_id,
            user_id=user_id,
        )
