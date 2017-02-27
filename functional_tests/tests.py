from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time


MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.driver.set_window_size(1120, 550)

    def tearDown(self):
        self.driver.quit()

    def check_for_row_in_grid(self, row_text):
        start_time = time.time()
        while True:
            try:
                grid = self.driver.find_element_by_id('id_bookshelf_grid')
                rows = grid.find_elements_by_tag_name('h2')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_bookshelf_and_retrieve_it_later(self):
        # Checkout the homepage
        self.driver.get(self.live_server_url)
        # Check the webpage title and header mention the book case
        self.assertIn("BookCase", self.driver.title)
        header_text = self.driver.find_element_by_tag_name('h1').text
        self.assertIn('BookCase', header_text)

        inputbox = self.driver.find_element_by_id('id_new_shelf')
        # Add a bookshelf "Want To Read"
        self.assertEqual(
            inputbox.get_attribute('placeholder'), 'Build a bookshelf'
        )
        # User types "Want To Read" into a text box
        inputbox.send_keys('Want To Read')

        # When hitting enter, the page updates,
        # and the page lists "Want To Read"
        inputbox.send_keys(Keys.ENTER)
        self.driver.get(self.live_server_url)

        self.check_for_row_in_grid('Want To Read')

        # Enters another bookshelf
        self.driver.get(self.live_server_url)
        inputbox = self.driver.find_element_by_id('id_new_shelf')
        inputbox.send_keys('Finished Books')
        inputbox.send_keys(Keys.ENTER)
        self.driver.get(self.live_server_url)

        self.check_for_row_in_grid('Finished Books')
        # User wonders if site will remember the list.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        self.driver.get(self.live_server_url)
        inputbox = self.driver.find_element_by_id('id_new_shelf')
        inputbox.send_keys('Want To Read')
        inputbox.send_keys(Keys.ENTER)
        #self.driver.get(self.live_server_url)

        #self.check_for_row_in_grid('Want To Read')
        # She sees the site has a unique URL for her --
        user_bookshelf_url = self.driver.current_url
        self.assertRegex(user_bookshelf_url, '/bookshelves/.+')

        #start process with new user
        self.tearDown()
        self.setUp()

        # Francis visits the home page.  There is no sign of Edith's
        # list
        self.driver.get(self.live_server_url)
        page_text = self.driver.find_element_by_tag_name('body').text
        # self.assertNotIn('Want To Read', page_text)

        # Francis starts a new list by entering a new item. He
        # is less interesting than Edith...
        inputbox = self.driver.find_element_by_id('id_new_shelf')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        #self.driver.get(self.live_server_url)
        #self.check_for_row_in_grid('Buy milk')

        # Francis gets his own unique URL
        francis_bookshelf_url = self.driver.current_url
        self.assertRegex(francis_bookshelf_url, '/bookshelves/.+')
        self.assertNotEqual(francis_bookshelf_url, user_bookshelf_url)

        # Again, there is no trace of Edith's list
        page_text = self.driver.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        # Visit the url - the book shelf is still there.
