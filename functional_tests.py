from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('BookCase', header_text)

        inputbox = self.browser.find_element_by_id('id_new_shelf')
        # Add a bookshelf "Want To Read"
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Build a bookshelf')
        # User types "Want To Read" into a text box
        inputbox.send_keys('Want To Read')

        # When hitting enter, the page updates, and the page lists "Want To Read"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        grid = self.browser.find_element_by_id('id_bookshelf_grid')
        rows = grid.find_elements_by_tag_name('h2')
        self.assertIn('Want To Read', [row.text for row in rows])
        self.fail('Finish the test!')





        # User wonders if site will remember the list.  She sees the site has a unique URL for her -- there is some explanatory text to that effect.

        # Visit the url - the book shelf is still there.

if __name__ == '__main__':
    unittest.main(warnings='ignore')
