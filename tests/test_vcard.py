import unittest
from pythonvCard4.vcard import Contact, ValidationError
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


class TestStructuredValues(unittest.TestCase):
    """An escaped separator inside a component must not split it."""

    def test_escaped_separators_parse_into_one_component(self):
        text = (
            "BEGIN:VCARD\nVERSION:4.0\nFN:John Doe\n"
            "N:Doe\\;Jr;John;;;\n"
            "ADR;TYPE=home:;;1\\; Main St;Town;;;\n"
            "CATEGORIES:R\\,D,Sales\n"
            "END:VCARD\n"
        )
        c = Contact.from_vcard(text)
        self.assertEqual(c.n, ["Doe;Jr", "John", "", "", ""])
        self.assertEqual(c.adr[0]["value"], ["", "", "1; Main St", "Town", "", "", ""])
        self.assertEqual(c.categories, ["R,D", "Sales"])

    def test_structured_values_round_trip(self):
        c = Contact(
            fn="John Doe",
            n=["Doe;Jr", "John", "", "", ""],
            nickname=["J;D"],
            adr=[{"value": ["", "", "1; Main St", "Town", "", "", ""], "type": ["home"]}],
            categories=["R,D", "Sales"],
        )
        parsed = Contact.from_vcard(c.to_vcard())
        self.assertEqual(parsed.n, c.n)
        self.assertEqual(parsed.nickname, c.nickname)
        self.assertEqual(parsed.adr[0]["value"], c.adr[0]["value"])
        self.assertEqual(parsed.categories, c.categories)


if __name__ == '__main__':
    unittest.main()
