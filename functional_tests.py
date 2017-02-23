from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_bookshelf_and_retrieve_it_later(self):
        # Checkout the homepage
        self.browser.get('http://localhost:8000')
        # Check the webpage title and header mention the book case
        self.assertIn("BookCase", self.browser.title)
        self.fail('Finish the test!')

        # Add a bookshelf "Want To Read"

        # User types "Wish List" into a text box

        # When hitting enter, the page updates, and the page lists "Want To Read"

        # User wonders if site will remember the list.  She sees the site has a unique URL for her -- there is some explanatory text to that effect.

        # Visit the url - the book shelf is still there.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
