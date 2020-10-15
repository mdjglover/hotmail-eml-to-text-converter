import quopri as qp
from bs4 import BeautifulSoup
from hotmail_eml_to_txt_converter.parser.Email import Email
from datetime import datetime

class HotmailEMLChainParser():
    # Parses .eml files downloaded from Hotmail into individual email objects.
    # Constructor takes a file object such as that returned by open()
    # Usage:
    # parsed_chain = HotmailEMLChainParser(file_object)
    # 
    # For emails in chain:
    # parsed_chain.get_emails()

    # For correspondents in chain:
    # parsed_chain.get_correspondents()
    
    def __init__(self, file_buffer):
        self._emails = []
        self._correspondents = {}

        if file_buffer is None:
            return

        decoded = qp.decodestring(file_buffer.read())
        decoded_utf = decoded.decode("utf-8")

        html_start_idx = decoded_utf.find("<html>")
        
        self._preamble = decoded_utf[:html_start_idx]
        self._html = decoded_utf[html_start_idx:].replace("&nbsp;", "")
        self._body_text = BeautifulSoup(self._html, "html.parser").get_text()

        self._current_position = 0

        self._parseChain()
    
    def get_emails(self):
        return self._emails
    
    def get_correspondents(self):
        return self._correspondents
    
    def _parseChain(self):
        # parses email chain and populates self.emails list
        # parse initial email
        next_email_index = self._find_next_email_index()

        builder = self.EmailBuilder(self._preamble, self._body_text[:next_email_index], is_first_in_chain=True)
        first_email = builder.build()
        self._correspondents[first_email.sender_email] = first_email.sender_name
        self._correspondents[first_email.receiver_email] = first_email.receiver_name
        self._emails.append(first_email)

        # parse remaining emails
        while next_email_index != -1:
            self._current_position = next_email_index

            head_start = next_email_index
            end_of_head = self._find_end_of_head()
            self._current_position = end_of_head

            next_email_index = self._find_next_email_index()

            builder = self.EmailBuilder(self._body_text[head_start:end_of_head], self._body_text[end_of_head:next_email_index])
            email = builder.build()
            email.sender_name = self._correspondents.get(email.sender_email, "")
            email.receiver_name = self._correspondents.get(email.receiver_email, "")
            self._emails.append(email)
    
    def _find_end_of_head(self):
        date_index = self._body_text.find("Date:", self._current_position)
        end_of_head_index = self._body_text.find("\n", date_index) + 1

        return end_of_head_index
    
    def _find_next_email_index(self):
        return self._body_text.find("From:", self._current_position)

    class EmailBuilder():
        # Takes email head and body as strings, along with bool
        # for whether it is the first email in chain and therefore
        # the preamble must be taken into account
        #
        # Preamble should be in format:
        #
        # MIME-Version: 1.0
        # Date: Sat, 1 Jan 2011 18:11:50 -0400
        # From: Foo <foo@bar.co.uk>
        # Subject: RE:
        # Thread-Topic: RE:
        # To: Bar <bar@foo.com>
        # Content-Transfer-Encoding: quoted-printable
        # Content-Type: text/html; charset="utf-8"
        #
        # Subsequent emails should be in format:
        #
        # From: bar@foo.com
        # To: foo@bar.co.uk
        # Subject: 
        # Date: Sat, 1 Jan 2011 14:50:14 +0000

        def __init__(self, head, body, is_first_in_chain=False):
            self._is_first_in_chain = is_first_in_chain
            self._head = head
            self._body = body
            self._email = Email()
            self._required_fields = ["To:", "From:", "Subject:", "Date:"]

        def build(self):
            # Builds email and returns Email object
            if self._head:
                self._parse_email()

            return self._email

        def _parse_email(self):
            head_items = self._head.split("\n")
            for item in head_items:
                if item == "":
                    continue
                
                field_end = item.find(":") + 1
                field = item[:field_end]
                if field in self._required_fields:
                    value = item[field_end:]
                    if field == "To:":
                        if self._is_first_in_chain:
                            name, email_address = self._parse_preamble_email(value)

                            self._email.sender_name = name
                            self._email.sender_email = email_address
                        else:
                            self._email.sender_email = value.strip()

                    elif field == "From:":
                        if self._is_first_in_chain:
                            name, email_address = self._parse_preamble_email(value)

                            self._email.receiver_name = name
                            self._email.receiver_email = email_address
                        else:
                            self._email.receiver_email = value.strip()

                    elif field == "Subject:":
                        self._email.subject = value.strip()
                    
                    elif field == "Date:":
                        self._email.datetime_hotmail_format = value.strip()
                        dt = self._create_datetime_from_hotmail_format(self._email.datetime_hotmail_format)
                        self._email.date = dt.strftime("%Y-%m-%d")
                        self._email.time = dt.strftime("%H-%M-%S")
                        
            self._email.body = self._body.strip()

        def _parse_preamble_email(self, email_field_value):
            email_address_start = email_field_value.index("<")
            name = email_field_value[:email_address_start].strip()
            email_address = email_field_value[email_address_start:].strip("<>")

            return (name, email_address)
        
        def _create_datetime_from_hotmail_format(self, hotmail_format_string):
            # Because %-d doesn't work in windows, these shenanigans must be done
            datetime_elements = hotmail_format_string.split(" ")
            day_of_month = int(datetime_elements[1])
            if day_of_month < 10:
                datetime_elements[1] = "0" + datetime_elements[1]
            datetime_string = " ".join(datetime_elements)
            # End of shenanigans
            dt = datetime.strptime(datetime_string, "%a, %d %b %Y %H:%M:%S %z")

            return dt

        

    
    