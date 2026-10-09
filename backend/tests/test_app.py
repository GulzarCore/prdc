import unittest

from app.main import clean_title


class TaskValidationTests(unittest.TestCase):
    def test_trims_whitespace(self):
        self.assertEqual(clean_title("  Learn Git  "), "Learn Git")

    def test_rejects_empty_title(self):
        with self.assertRaises(ValueError):
            clean_title("   ")

    def test_rejects_title_over_200_characters(self):
        with self.assertRaises(ValueError):
            clean_title("x" * 201)

    def test_accepts_200_characters(self):
        self.assertEqual(len(clean_title("x" * 200)), 200)


if __name__ == "__main__":
    unittest.main()

from app.main import version

# Add this method inside TaskValidationTests:
def test_version(self):
    self.assertEqual(
        version(),
        {"app": "devops-lab", "version": "1.0.0"},
    )