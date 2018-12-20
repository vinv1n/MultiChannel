import smtplib
import logging
import os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


logger = logging.getLogger(__name__)


class EmailHandler:

    def __init__(self, password, address, host=None, port=587):

        if host:
            self.server = smtplib.SMTP(host=host, port=port)
        else:
            self.server = smtplib.SMTP("smtp.gmail.com", port=587)

        self.password = password
        self.user = address

        # TODO check if is always needed
        self._login()

    def _login(self):
        self.server.starttls()
        self.server.login(user=self.user, password=self.password)

    def _quit(self):
        self.server.quit()

    def send_message(self, text, receivers, msg_type):
        for receiver in receivers:
            toaddr = receiver.get("address")
            if msg_type == "seen":
                formatted_message = self._format_message(toaddr, text, seen=True)
            else:
                formatted_message = self._format_message(toaddr, text)

            self.server.sendmail(self.user, to_addrs=toaddr, msg=formatted_message)

    def get_status(self):
        pass

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
