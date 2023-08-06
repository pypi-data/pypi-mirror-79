import unittest
import sethealth


class TestAPI(unittest.TestCase):
    def test_valid(self):
        client = sethealth.Client()
        token = client.getToken()
        self.assertGreater(len(token), 10)

    def test_valid_options(self):
        client = sethealth.Client()
        token = client.getToken(test_mode=True, user_id="user")
        self.assertGreater(len(token), 10)

    def test_unvalid(self):
        with self.assertRaises(sethealth.AuthException):
            client = sethealth.Client("", "")
            client.getToken()

    def test_missing_key(self):
        with self.assertRaises(sethealth.InputException):
            sethealth.Client(None, "Secret")

    def test_missing_secret(self):
        with self.assertRaises(sethealth.InputException):
            sethealth.Client("Key", None)


if __name__ == "__main__":
    unittest.main()
