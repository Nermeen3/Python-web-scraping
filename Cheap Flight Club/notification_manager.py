from twilio.rest import Client

class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.account_sid = "ABC"
        self.auth_token = "ABC"
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self):
        message_body = f"Low Price Alert!\n"
        message = self.client.messages.create(
            body=message_body,
            from_='+11111111111',
            to='+22222222222'
        )
        print(message.sid)


