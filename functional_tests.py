from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self) -> None:
        self.browser = webdriver.Firefox()
        return super().setUp()

    def tearDown(self) -> None:
        self.browser.quit()
        return super().tearDown()

    def test_can_start_a_list_and_retrieve_it_later(self):    

        # Edith has heard about a cool, new, online to-do app. 
        # She goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # She notices the page title and header mention to-do lists.
        self.assertIn('Todo', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1')
        self.assertIn('Tood', header_text)
        self.fail('Finish the test!')

        # She is invited to enter a todo item straight away. 
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a todo item'
        )

        # She types "buy peacock feathers" into a text box.
        # (Edith's hobby is fly-fishing lures.)
        inputbox.send_keys('Buy peacock feathers')        

        # When she hits enter the page updates. 
        # Now the page lists a todo item: 
        # "1: Buy peacock feathers"

        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_id('tr')
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows)
        )

        # There is still a text box inviting her to add another item.
        # She enters:
        # "Use peacock feathers to make a fly"
        # (Edith is very methodical.)

        send.fail('Finish the test!')

        # She visits that URL - her todo list is still there.

        # Satisfied, she goes back to sleep. 

if __name__ == '__main__':
    unittest.main()