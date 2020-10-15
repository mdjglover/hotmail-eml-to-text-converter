class Email():
    # Simple object to hold email data

    def __init__(self):
        self.sender_name = ""
        self.sender_email = ""

        self.receiver_name = ""
        self.receiver_email = ""

        self.date = ""
        self.time = ""
        self.datetime_hotmail_format = ""

        self.subject = ""
        self.body = ""

    def __str__(self):
        output =  f"From: {self.sender_name} <{self.sender_email}>\n"
        output += f"To: {self.receiver_name} <{self.receiver_email}>\n"
        output += f"Subject: {self.subject}\n"
        output += f"Date: {self.datetime_hotmail_format}\n"
        output += f"-------------------------------------------------------------\n"
        output += f"\n"
        output += f"{self.body}"

        return output