from twilio.rest import Client

class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.account_sid = "AC8d94d30af05d44101787ca272e41de56"
        self.auth_token = "416c08a8fd0b9991f2749587b890a9e0"
        self.client = Client(self.account_sid, self.auth_token)

    def send_sms(self):
        message_body = f"Low Price Alert!\n"
        message = self.client.messages.create(
            body=message_body,
            from_='+19283707954',
            to='+995558871331'  # 995593319561
        )
        print(message.sid)


