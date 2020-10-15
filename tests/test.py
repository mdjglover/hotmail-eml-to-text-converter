import sys
import os
sys.path.append(os.path.abspath("."))

import unittest
from hotmail_eml_to_txt_converter.parser.HotmailEMLChainParser import HotmailEMLChainParser


class test_HotmailEMLChainParser(unittest.TestCase):
    def test_parser_one_email(self):
        emails = []
        correspondents = {}
        with open("Z:/dev/projects/eml-to-text-converter/tests/test-source/test_one_email.eml") as f:
            parser = HotmailEMLChainParser(f)
            emails = parser.get_emails()
            correspondents = parser.get_correspondents()
        
        self.assertEqual(len(emails), 1)
        self.assertIn("person_one@hotmail.com", correspondents)
        self.assertIn("person_two@hotmail.com", correspondents)
        self.assertIn("Cyril", emails[0].body)
        self.assertEqual("18-11-50", emails[0].time)

    def test_parser_two_emails(self):
        emails = []
        correspondents = {}
        with open("Z:/dev/projects/eml-to-text-converter/tests/test-source/test_two_emails.eml") as f:
            parser = HotmailEMLChainParser(f)
            emails = parser.get_emails()
            correspondents = parser.get_correspondents()
        
        self.assertEqual(len(emails), 2)
        self.assertIn("person_one@hotmail.com", correspondents)
        self.assertIn("person_two@hotmail.com", correspondents)
        self.assertIn("Cyril", emails[0].body)
        self.assertIn("Happy", emails[1].body)
        self.assertEqual("18-11-50", emails[0].time)
        self.assertEqual("14-50-14", emails[1].time)

if __name__ == '__main__':
    unittest.main()

