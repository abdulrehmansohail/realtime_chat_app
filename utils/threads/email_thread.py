# Description: This file contains the EmailThread class which is used to send emails asynchronously
import logging as loggers
from threading import Thread
from django.conf import settings
from django.core.mail import EmailMessage
from django.template.loader import get_template

loggers.basicConfig(level=loggers.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = loggers.getLogger(__name__)


class EmailThread(Thread):
    """
    This class is used to send emails asynchronously.

    Attributes:
        subject (str): The subject of the email.
        html_content (str): The content of the email.
        recipient_list (list): The list of recipients.

    """

    def __init__(self, subject, html_content, recipient_list, key, files=None):
        self.subject = subject
        self.key = key
        self.recipient_list = recipient_list
        self.html_content = html_content
        self.files = files
        Thread.__init__(self)

    def run(self):
        """ This Function used for run the thread """
        try:

            message = get_template(self.html_content).render(self.key)
            msg = EmailMessage(self.subject, message, settings.FROM_EMAIL, self.recipient_list)
            msg.content_subtype = "html"

            msg.send()
        except Exception as exception:
            logger.error("%s", exception)


def send_mail(subject, html_content, recipient_list, key=None, files=None):
    """ This module is used for send email in the whole system.
        This function run asynchronously.
        Args:
            subject (str): The subject of the email.
            html_content (str): The content of the email.
            recipient_list (list): The list of recipients.
            key (dict): The dictionary of key value pairs.
            files (list): The list of files.
       """
    try:
        EmailThread(subject, html_content, recipient_list, key, files).start()
        logger.info(("Email sent to:%s", recipient_list))
    except Exception as exception:
        logger.error(exception)
