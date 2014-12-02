
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings
import dkim # http://hewgill.com/pydkim

class DKIMBackend(EmailBackend):
    def _send(self, email_message):
        """A helper method that does the actual sending + DKIM signing."""
        if not email_message.recipients():
            return False
        try:
            print "xxxxxxxxxxxxxxxxxxxxxxxxEMAIL"
            message_string = email_message.message().as_string()
            signature = dkim.sign(message_string,
                                  settings.DKIM_SELECTOR,
                                  settings.DKIM_DOMAIN,
                                  settings.DKIM_PRIVATE_KEY)
            self.connection.sendmail(email_message.from_email,
                    email_message.recipients(),
                    signature+message_string)
        except:
            if not self.fail_silently:
                raise
            return False
        return True
