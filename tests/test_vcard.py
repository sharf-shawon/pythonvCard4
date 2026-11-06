import unittest
from pythonvCard4.vcard import Contact, ValidationError, escape_text, unescape_text
from datetime import date

class TestContact(unittest.TestCase):
    def test_round_trip(self):
        c = Contact(
            fn="Alice",
            email=[ {"value":"alice@example.com", "type":["work"]} ],
            tel=[ {"value":"+1234567890","type":["cell"]} ],
            bday=date(1990,1,1)
        )
        text = c.to_vcard()
        parsed = Contact.from_vcard(text)
        self.assertEqual(parsed.fn, "Alice")
        self.assertEqual(parsed.email[0]["value"], "alice@example.com")
        self.assertEqual(parsed.bday, date(1990,1,1))

    def test_missing_fn(self):
        with self.assertRaises(ValidationError):
            Contact(fn="").to_vcard()

if __name__ == '__main__':
    unittest.main()


class TestUnescapeText(unittest.TestCase):
    def test_escaped_backslash_before_n_is_not_a_newline(self):
        # "\\n" on the wire is an escaped backslash, then a literal "n".
        self.assertEqual(unescape_text("a\\\\nb"), "a\\nb")

    def test_escaped_backslash_before_separators_is_kept(self):
        self.assertEqual(unescape_text("C:\\\;x"), "C:\;x")
        self.assertEqual(unescape_text("C:\\\\,x"), "C:\\,x")

    def test_uppercase_n_is_a_newline(self):
        self.assertEqual(unescape_text("a\\Nb"), "a\nb")

    def test_round_trips_escape_text(self):
        for text in ["a\\nb", "C:\\", "x;y,z", "line1\nline2", "\\\\", "\;\\,"]:
            with self.subTest(text=text):
                self.assertEqual(unescape_text(escape_text(text)), text)
