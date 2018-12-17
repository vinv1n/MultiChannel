import smtplib
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


logger = logging.getLogger(__name__)


class EmailHandler:

    def __init__(self, password, address, host=None):

        if host:
            self.server = smtplib.SMTP(host=host, port=587)

        self.password = password
        self.user = address

        self.server = smtplib.SMTP("smtp.gmail.com", port=587)

        # TODO check if is always needed
        self._login()

    def _login(self):
        self.server.starttls()
        self.server.login(user=self.user, password=self.password)

    def _quit(self):
        self.server.quit()

    def send_message(self, text, receivers, attachments=None):
        for receiver in receivers:
            toaddr = receiver.get("address")
            formatted_message = self._format_message(toaddr, text)
            self.server.sendmail(self.user, to_addrs=toaddr, msg=formatted_message)

    def get_status(self):
        pass

    def _format_message(self, receiver, text):
        message = MIMEMultipart()

        # handle the addresses
        message['From'] = self.user
        message['To'] = receiver.get("address")

        message['Subject'] = text.get("subject")

        message.attach(MIMEText(text.get('body'), 'plain'))

        string = message.as_string()
        return string